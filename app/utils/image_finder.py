from app.services.faculty_image_service import fetch_faculty_data
from app.utils.name_normalizer import normalize_name


def find_image_url(faculty_name: str):
    """
    Finds the PSG image URL for a faculty.
    Returns None if no matching faculty is found.
    """

    normalized_name = normalize_name(faculty_name)

    faculty_list = fetch_faculty_data()

    for faculty in faculty_list:

        if normalize_name(faculty["name"]) == normalized_name:
            return faculty["image_url"]

    return None