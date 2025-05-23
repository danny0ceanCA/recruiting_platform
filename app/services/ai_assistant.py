import os
import openai
from app.schemas.student import StudentCreate
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(student: StudentCreate) -> str:
    prompt = f"""
    Write a professional summary for a healthcare student using the details below.
    The tone should be confident, caring, and suitable for school-based healthcare settings.

    First Name: {student.first_name}
    Last Name: {student.last_name}
    License Type: {student.license_type}
    Job Goals: {student.job_goals}
    Availability: {student.availability}
    Transportation: {student.transportation}
    Experience: {student.experience}
    Soft Skills: {student.soft_skills}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a healthcare recruiter assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI Summary unavailable: {str(e)}"
