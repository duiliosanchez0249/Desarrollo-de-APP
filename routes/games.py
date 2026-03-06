from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from core.database import get_session
from models.game import Game
import redis, json, shutil, os

router = APIRouter(prefix="/games", tags=["Games"])

# Conexión a Redis (con manejo de errores por si no tienes Docker prendido)
try:
    rd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
except:
    rd = None

@router.post("/")
def create_game(game: Game, session: Session = Depends(get_session)):
    session.add(game)
    session.commit()
    session.refresh(game)
    return game

@router.get("/")
def read_games(session: Session = Depends(get_session)):
    return session.exec(select(Game)).all()

@router.get("/top-rated")
def get_top_games(session: Session = Depends(get_session)):
    if rd:
        try:
            cached = rd.get("top_games")
            if cached: return json.loads(cached)
            games = session.exec(select(Game).where(Game.rating >= 9)).all()
            rd.setex("top_games", 60, json.dumps([g.dict() for g in games]))
            return games
        except: pass
    return session.exec(select(Game).where(Game.rating >= 9)).all()

@router.post("/{game_id}/upload")
async def upload_cover(game_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    game = session.get(Game, game_id)
    if game:
        game.cover_image = path
        session.commit()
    return {"path": path}
