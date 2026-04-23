from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .auth import router as auth_router
from .lessons import router as lessons_router
from .payments import router as payments_router
from .progress import router as progress_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clone Mastery Backend")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(lessons_router)
app.include_router(payments_router)
app.include_router(progress_router)

@app.get("/")
def home():
    return {"message": "Backend is running"}
