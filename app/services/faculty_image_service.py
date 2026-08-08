from bs4 import BeautifulSoup
from pathlib import Path


# Base URL where PSG stores faculty images
BASE_IMAGE_URL = "https://www.psgtech.edu/educms/upload/faculty/"


def fetch_faculty_data():
    """
    Parses the saved PSG faculty HTML page and extracts:
    - Faculty Name
    - Faculty Image Code
    - Faculty Image URL

    Returns:
        List[dict]
    """

    html_path = Path("data/faculty1.html")

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    faculty_data = []

    # Every faculty card contains one profile div
    profiles = soup.find_all("div", class_="profile")

    for profile in profiles:

        # Find the row containing this faculty
        card = profile.find_parent("div", class_="row")

        if card is None:
            continue

        # Find the faculty image
        img = card.find("img")

        if img is None:
            continue

        # Extract faculty name
        name = profile.get_text(strip=True)

        # Example:
        # ./faculty1_files/C5816
        image_code = Path(img["src"]).name

        # Actual PSG image URL
        image_url = BASE_IMAGE_URL + image_code

        faculty_data.append(
            {
                "name": name,
                "image_code": image_code,
                "image_url": image_url,
            }
        )

    return faculty_data