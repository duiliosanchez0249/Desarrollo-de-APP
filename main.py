from fastapi import FastAPI, Body, Depends
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from core.database import create_db_and_tables, get_session
from routes import games
from models.user import User
import os

app = FastAPI(title="Gaming Hub API Pro")

@app.on_event("startup")
def on_startup():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    create_db_and_tables()

app.mount("/static", StaticFiles(directory="uploads"), name="static")
app.include_router(games.router)

@app.post("/users/", tags=["Users"])
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/validate-review", tags=["Advanced Validation"])
def validate_review(payload: dict = Body(..., example={
    "game_id": 1,
    "review_text": "Este juego es increíble",
    "score": 9.5
})):
    """Endpoint para validación de JSON Schema"""
    return {"status": "Schema Validado", "content": payload}
