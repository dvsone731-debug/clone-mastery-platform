from fastapi import APIRouter, Header
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import LessonProgress
from .roles import require_role

router = APIRouter(prefix="/progress", tags=["Progress"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{lesson_id}")
def mark_complete(lesson_id: int, authorization: str = Header(None), db: Session = next(get_db())):
    data = require_role(authorization, ["free", "pro", "admin"])

    progress = LessonProgress(
        user_id=data["id"],
        lesson_id=lesson_id,
        completed=True
    )

    db.add(progress)
    db.commit()

    return {"message": "Lesson marked complete"}

@router.get("/")
def get_user_progress(authorization: str = Header(None), db: Session = next(get_db())):
    data = require_role(authorization, ["free", "pro", "admin"])

    items = db.query(LessonProgress).filter(LessonProgress.user_id == data["id"]).all()

    return {"progress": [{"lesson_id": p.lesson_id, "completed": p.completed} for p in items]}
