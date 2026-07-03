import os
from dotenv import load_dotenv
import httpx

load_dotenv()

async def send_verification_email(email: str, code: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": os.getenv("BREVO_API_KEY"),
                "Content-Type": "application/json"
            },
            json={
                "sender": {"name": "AI Interview", "email": "aivonwelcome@gmail.com"},
                "to": [{"email": email}],
                "subject": "Код подтверждения",
                "textContent": f"Ваш код подтверждения: {code}\n\nКод действителен 5 минут."
            }
        )
        