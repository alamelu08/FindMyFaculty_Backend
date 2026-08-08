from app.services.faculty_image_service import fetch_faculty_data
from app.utils.name_normalizer import normalize_name

faculty = fetch_faculty_data()

for f in faculty:
    print(
        f["name"],
        " ---> ",
        normalize_name(f["name"])
    )