import pdfplumber
from datetime import time
from sqlalchemy.orm import Session

from app.models.period import Period
from app.models.faculty import Faculty
from app.models.faculty_timetable import FacultyTimetable


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

        page = pdf.pages[0]

        tables = page.extract_tables()

        timetable = tables[0]
        faculty_table = tables[1]

        # -------------------------
        # Create Faculty Map
        # -------------------------
        faculty_map = {}

        for row in faculty_table[1:]:

            if not row or len(row) < 2:
                continue

            faculty_id = row[0].strip()
            faculty_name = row[1].strip()

            faculty_map[faculty_id] = faculty_name
        print("Faculty Map:")
        print(faculty_map)

        # -------------------------
        # Save Faculty
        # -------------------------
        for faculty_id, faculty_name in faculty_map.items():
            print("Reading:", faculty_id, faculty_name)
            existing = (
                db.query(Faculty)
                .filter(Faculty.id == faculty_id)
                .first()
            )

            if existing:
                # If it was previously created as Unknown, update the name
                if existing.name == "Unknown":
                    existing.name = faculty_name
                continue

            db.add(
                Faculty(
                    id=faculty_id,
                    name=faculty_name,
                    cabin="-",
                    image_url=None,
                    cabin_directions=None
                )
            )

        db.commit()

        # -------------------------
        # Parse Timetable
        # -------------------------
        for row in timetable[2:]:

            day = row[0]

            print(f"\nProcessing {day}")

            for period_no in range(1, len(row)):

                cell = row[period_no]

                if not cell:
                    continue

                cell = cell.strip()

                # Skip Library periods
                if cell.upper() == "LIB":
                    continue

                faculty_text = ""
                room = ""

                parts = cell.split("\n")

                for part in parts:

                    part = part.strip()

                    if not part:
                        continue

                    # Room
                    if part.startswith("Y") or part.startswith("Q") or part == "*":
                        room = part
                    else:
                        if faculty_text == "":
                            faculty_text = part
                        else:
                            faculty_text += "/" + part

                faculty_ids = faculty_text.split("/")

                for faculty_id in faculty_ids:

                    faculty_id = faculty_id.strip()

                    if faculty_id == "":
                        continue

                    records.append(
                        {
                            "faculty_id": faculty_id,
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
    # Save Timetable
    # -------------------------
    for record in records:

        faculty = (
            db.query(Faculty)
            .filter(Faculty.id == record["faculty_id"])
            .first()
        )

    # Faculty doesn't exist -> create it
        if faculty is None:

            faculty = Faculty(
                id=record["faculty_id"],
                name="Unknown",
                cabin="-",
                image_url=None,
                cabin_directions=None
            )

            db.add(faculty)
            db.commit()
            db.refresh(faculty)

            print(f"Created faculty {record['faculty_id']}")

        timetable = FacultyTimetable(
            faculty_id=faculty.id,
            day=record["day"],
            period_no=record["period_no"],
            room=record["room"] if record["room"] else "-"
        )

        db.add(timetable)
        saved += 1

    db.commit()

    return {
        "message": "Timetable uploaded successfully",
        "saved_records": saved,
        "skipped_records": skipped
    }