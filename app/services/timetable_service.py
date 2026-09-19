import pdfplumber
from datetime import time
from sqlalchemy.orm import Session

from app.models.period import Period
from app.models.faculty import Faculty
from app.models.faculty_timetable import FacultyTimetable
from app.utils.uuid_generator import generate_faculty_uuid
from app.utils.image_finder import find_image_url


# ----------------------------------------
# Create Periods Automatically
# ----------------------------------------
def create_periods(db: Session):

    periods = [
        (1, time(8, 30), time(9, 20)),
        (2, time(9, 20), time(10, 10)),
        (3, time(10, 30), time(11, 20)),
        (4, time(11, 20), time(12, 10)),
        (5, time(13, 40), time(14, 30)),
        (6, time(14, 30), time(15, 20)),
        (7, time(15, 30), time(16, 20)),
        (8, time(16, 20), time(17, 10)),
    ]

    for period_no, start, end in periods:

        existing = (
            db.query(Period)
            .filter(Period.period_no == period_no)
            .first()
        )

        if existing:
            continue

        db.add(
            Period(
                period_no=period_no,
                start_time=start,
                end_time=end
            )
        )

    db.commit()


# ----------------------------------------
# Upload Timetable
# ----------------------------------------
def upload_timetable_service(file_path, db: Session):

    # Create periods if they don't exist
    create_periods(db)

    records = []

    with pdfplumber.open(file_path) as pdf:
        if not pdf.pages:
            return {"message": "Empty PDF file", "saved_records": 0, "skipped_records": 0}

        page0_tables = pdf.pages[0].extract_tables()
        if not page0_tables:
            return {"message": "No tables found in PDF", "saved_records": 0, "skipped_records": 0}

        # -------------------------------------------------------------
        # Format 1: Timetable in tables[0], Faculty Map in tables[1]
        # (Table 1 has columns ['Fac ID', 'Faculty Name'])
        # -------------------------------------------------------------
        if len(page0_tables) == 2 and any("Fac ID" in str(c) for c in (page0_tables[1][0] or [])):
            timetable = page0_tables[0]
            faculty_table = page0_tables[1]

            code_to_name = {}
            for row in faculty_table[1:]:
                if not row or len(row) < 2:
                    continue
                fid = row[0].strip()
                fname = row[1].strip()
                code_to_name[fid] = fname

            # Check remaining pages for faculty mappings if present
            if len(pdf.pages) > 1:
                for p in pdf.pages[1:]:
                    extra_tables = p.extract_tables()
                    for t in extra_tables:
                        for row in t:
                            if row and len(row) >= 2 and row[0] and row[1]:
                                code_to_name[row[0].strip()] = row[1].strip()

            # Always create/map to deterministic UUIDs for all faculty
            code_to_uuid = {}
            for fid, fname in code_to_name.items():
                fac_uuid = generate_faculty_uuid(fname)
                code_to_uuid[fid] = fac_uuid

                existing = db.query(Faculty).filter(Faculty.id == fac_uuid).first()
                if existing:
                    if existing.name != fname:
                        existing.name = fname
                    if not existing.image_url:
                        existing.image_url = find_image_url(fname)
                else:
                    db.add(
                        Faculty(
                            id=fac_uuid,
                            name=fname,
                            cabin="-",
                            image_url=find_image_url(fname),
                            cabin_directions=None
                        )
                    )
            db.commit()

            for row in timetable[2:]:
                day = row[0]
                if not day:
                    continue

                for period_no in range(1, len(row)):
                    cell = row[period_no]
                    if not cell:
                        continue

                    cell = cell.strip()
                    if cell.upper() == "LIB":
                        continue

                    faculty_text = ""
                    room = ""
                    parts = cell.split("\n")

                    for part in parts:
                        part = part.strip()
                        if not part:
                            continue

                        if part.startswith("Y") or part.startswith("Q") or part == "*":
                            room = part
                        else:
                            if faculty_text == "":
                                faculty_text = part
                            else:
                                faculty_text += "/" + part

                    for fid in faculty_text.split("/"):
                        fid = fid.strip()
                        if fid == "":
                            continue

                        target_uuid = code_to_uuid.get(fid) or generate_faculty_uuid(fid)

                        records.append(
                            {
                                "faculty_id": target_uuid,
                                "day": day,
                                "period_no": period_no,
                                "room": room
                            }
                        )

        # -------------------------------------------------------------
        # Format 2: Official College Timetable with Course Code / Staff Table
        # -------------------------------------------------------------
        else:
            for page in pdf.pages:
                tables = page.extract_tables()
                if not tables:
                    continue

                tt_table = None
                course_table = None
                for t in tables:
                    if len(t) >= 7 and any("MON" in str(row[0]) for row in t if row and row[0]):
                        tt_table = t
                    elif len(t) >= 1 and any("COURSE CODE" in str(c) for c in (t[0] or [])):
                        course_table = t

                if not tt_table:
                    continue

                course_to_staff = {}
                if course_table:
                    codes = [c.strip() for c in course_table[0][0].split("\n") if c.strip()][1:]
                    staffs = [s.strip() for s in course_table[0][2].split("\n") if s.strip()][1:]
                    for c, s in zip(codes, staffs):
                        if c not in course_to_staff:
                            course_to_staff[c] = []
                        if s not in course_to_staff[c]:
                            course_to_staff[c].append(s)

                for row in tt_table[2:]:
                    day = row[0]
                    if not day:
                        continue

                    for period_no in range(1, len(row)):
                        cell = row[period_no]
                        if not cell:
                            continue

                        cell = cell.strip()
                        if cell.upper() == "LIB":
                            continue

                        parts = [p.strip() for p in cell.split("\n") if p.strip()]
                        room = "-"
                        courses = []

                        for part in parts:
                            if part.startswith("Y") or part.startswith("Q") or part == "*":
                                room = part
                            else:
                                courses.append(part)

                        for course in courses:
                            staff_list = course_to_staff.get(course, [course])
                            for staff in staff_list:
                                fac_uuid = generate_faculty_uuid(staff)
                                records.append(
                                    {
                                        "faculty_id": fac_uuid,
                                        "staff_name": staff,
                                        "day": day,
                                        "period_no": period_no,
                                        "room": room
                                    }
                                )

    # -------------------------
    # Delete Old Timetable
    # -------------------------
    db.query(FacultyTimetable).delete()
    db.commit()

    saved = 0
    skipped = 0

    # -------------------------
    # Save Timetable Records
    # -------------------------
    for record in records:
        faculty_id = record["faculty_id"]
        staff_name = record.get("staff_name")

        faculty = (
            db.query(Faculty)
            .filter(Faculty.id == faculty_id)
            .first()
        )

        if faculty is None:
            name = staff_name if staff_name else "Unknown"
            faculty = Faculty(
                id=faculty_id,
                name=name,
                cabin="-",
                image_url=find_image_url(name) if staff_name else None,
                cabin_directions=None
            )
            db.add(faculty)
            db.commit()
            db.refresh(faculty)
        elif faculty.image_url is None and staff_name:
            img = find_image_url(staff_name)
            if img:
                faculty.image_url = img
                db.commit()

        if faculty:
            timetable = FacultyTimetable(
                faculty_id=faculty.id,
                day=record["day"],
                period_no=record["period_no"],
                room=record["room"] if record["room"] else "-"
            )
            db.add(timetable)
            saved += 1
        else:
            skipped += 1

    db.commit()

    return {
        "message": "Timetable uploaded successfully",
        "saved_records": saved,
        "skipped_records": skipped
    }