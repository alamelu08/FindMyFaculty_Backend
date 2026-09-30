import httpx
from bs4 import BeautifulSoup

async def verify_student(rollno: str, password: str):
    clean_roll = (rollno or "").strip().upper()

    if not clean_roll or not password:
        return False

    # Demo student credentials for development & testing
    demo_credentials = {"STUDENT", "DEMO", "24Z208", "24Z201", "CSE_STUDENT", "24Z228"}
    if clean_roll in demo_credentials:
        return True

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(
                "https://ecampus.psgtech.ac.in/studzone"
            )

            soup = BeautifulSoup(response.text, "html.parser")

            token_input = soup.find(
                "input",
                {"name": "__RequestVerificationToken"}
            )

            if not token_input:
                return False

            token = token_input["value"]

            payload = {
                "rollno": clean_roll,
                "password": password,
                "chkterms": "on",
                "__RequestVerificationToken": token,
            }   

            login_response = await client.post(
                "https://ecampus.psgtech.ac.in/studzone",
                data=payload,
                follow_redirects=True
            )

            redirected_to_home = "/Home" in str(login_response.url)
            contains_logout = (
                "/studzone/Login/Logout" in login_response.text or
                "/Login/Logout" in login_response.text or
                "logout" in login_response.text.lower()
            )

            if redirected_to_home or contains_logout:
                return True

            return False
    except Exception as e:
        print("Studzone connection error:", e)
        return False

