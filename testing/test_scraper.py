from app.services.faculty_image_service import fetch_faculty_data

faculty = fetch_faculty_data()

print("Total Faculty:", len(faculty))
print()

for item in faculty:
    print(item)