from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import videos, shorts, posters

app = FastAPI(
    title="Mahnoor Portfolio API",
    description="Backend API for managing video links, shorts, and poster uploads.",
    version="2.0.0"
)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(videos.router)
app.include_router(shorts.router)
app.include_router(posters.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Mahnoor Portfolio API - MongoDB Edition"}
