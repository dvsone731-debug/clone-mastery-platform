from fastapi import APIRouter, Header
import json
from .roles import require_role

router = APIRouter(prefix="/lessons", tags=["Lessons"])

with open("course/course.json") as f:
    COURSE = json.load(f)

@router.get("/")
def get_course():
    return COURSE

@router.get("/{lesson_id}")
def get_lesson(lesson_id: int, authorization: str = Header(None)):
    require_role(authorization, ["free", "pro", "admin"])

    try:
        with open(f"course/lessons/lesson-{lesson_id}.txt") as f:
            return {"id": lesson_id, "content": f.read()}
    except:
        return {"error": "Lesson not found"}
