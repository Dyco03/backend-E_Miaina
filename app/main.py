from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import users, challenges, community, chatbot
from db.database import engine, Base
from db.models import users as user_models, challenges as challenge_models, community as community_models, chatbot as chatbot_models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Eaina API",
    description="Backend API for Eaina application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(challenges.router)
app.include_router(community.router)
app.include_router(chatbot.router)

@app.get("/")
def root():
    return {"message": "Welcome to Eaina API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)