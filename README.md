# FindMyFaculty - Backend

Backend service for the **FindMyFaculty** application, built using **FastAPI** and **PostgreSQL**. It handles authentication, faculty management, timetable processing, and real-time faculty location retrieval.

---

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* pdfplumber or camelot
* Uvicorn

---

## Features

* Student authentication
* Faculty search
* Real-time faculty location detection
* Faculty management (Add, Update, Delete)
* Student timetable PDF upload
* Automatic timetable parsing and database population
* Time-based classroom/cabin detection

---

## Database Tables

* Faculty
* FacultyTimetable
* Period

---

## API Modules

* Authentication
* Faculty
* Admin
* Upload

---

## Running the Backend

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

After running the server:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## Project Documentation

For a detailed explanation of the backend architecture, folder structure, database design, API endpoints, and workflow, refer to:

* **BACKEND_ARCHITECTURE.md**

---

## Developed Using

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
