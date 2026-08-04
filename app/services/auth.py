import httpx
from bs4 import BeautifulSoup

async def verify_student(rollno: str, password: str):
    async with httpx.AsyncClient() as client:

        response = await client.get(
            "https://ecampus.psgtech.ac.in/studzone"
        )

        soup = BeautifulSoup(response.text, "html.parser")

        token_input = soup.find(
            "input",
            {"name": "__RequestVerificationToken"}
        )

        token = token_input["value"]

        print(token)

        payload = {
        "rollno": rollno,
        "password": password,
        "chkterms": "on",
        "__RequestVerificationToken": token,
        }   

        login_response = await client.post(
        "https://ecampus.psgtech.ac.in/studzone",
        data=payload,
        follow_redirects=True
        )

        if "/Login/Logout" in login_response.text:
            return True
        return False

