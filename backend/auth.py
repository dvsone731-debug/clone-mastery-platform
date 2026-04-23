from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .database import SessionLocal
from .models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET = "SUPER_SECRET_KEY"
ALGO = "HS256"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(data, SECRET, algorithm=ALGO)

@router.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already exists")

    user = User(email=email, password=pwd.hash(password))
    db.add(user)
    db.commit()

    return {"message": "Account created"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd.verify(password, user.password):
        raise HTTPException(400, "Invalid credentials")

    token = create_token({"id": user.id, "role": user.role})

    return {"token": token, "role": user.role}
