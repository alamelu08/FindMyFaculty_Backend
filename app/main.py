from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.database.database import Base, engine
from app.models import faculty, period, faculty_timetable
from app.routers import admin,faculty,login,login_admin


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(admin.router)
app.include_router(faculty.router)
app.include_router(login.router)
app.include_router(login_admin.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FindMyFaculty API",
        version="1.0.0",
        description="FindMyFaculty Backend API",
        routes=app.routes,
    )
    # Remove 422 Validation Error from all endpoints in Swagger docs
    for path in openapi_schema.get("paths", {}).values():
        for method in path.values():
            if isinstance(method, dict) and "responses" in method:
                method["responses"].pop("422", None)
    # Remove ValidationError and HTTPValidationError from components
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
        openapi_schema["components"]["schemas"].pop("ValidationError", None)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "FindMyFaculty Backend is running!"}

# from fastapi import FastAPI
# from app.database.database import Base, engine
# from app.models import faculty, period, faculty_timetable
# from app.routers import admin,faculty



# app = FastAPI()

# app.include_router(admin.router)
# app.include_router(faculty.router)

# Base.metadata.create_all(bind=engine)

# @app.get("/")
# def root():
#     return {"message": "Hello"}