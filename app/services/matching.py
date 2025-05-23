import json
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.student import Student
from app.services.embedding import get_embedding
import numpy as np

def cosine_similarity(a: List[float], b: List[float]) -> float:
    a_np, b_np = np.array(a), np.array(b)
    return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))

def match_students_to_job(job_description: str, db: Session) -> List[Dict]:
    job_embedding = get_embedding(job_description)
    if not job_embedding:
        return []

    matched = []

    students = db.query(Student).all()
    for student in students:
        if not student.embedding:
            continue

        try:
            student_embedding = json.loads(student.embedding)
            score = cosine_similarity(job_embedding, student_embedding)
            matched.append({
                "student": student,
                "match_score": round(score, 4)
            })
        except Exception as e:
            print(f"⚠️ Skipping student ID {student.id}: {e}")

    # Sort by descending score
    matched.sort(key=lambda x: x["match_score"], reverse=True)
    return matched
