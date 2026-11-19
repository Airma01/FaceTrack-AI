import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings


# Initialize FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FaceTrack-AI Attendance Management API",
    debug=settings.DEBUG,
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to FaceTrack-AI",
        "status": "running",
        "version": settings.APP_VERSION,
    }


# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
    }


# Run application
if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )