from fastapi import APIRouter, Header, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
from .roles import require_role

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upgrade")
def upgrade_to_pro(authorization: str = Header(None), db: Session = next(get_db())):
    data = require_role(authorization, ["free", "pro", "admin"])

    user = db.query(User).filter(User.id == data["id"]).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.role = "pro"
    db.commit()

    return {"message": "Upgraded to PRO"}
