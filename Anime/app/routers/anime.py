from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import cast, Integer, Float, and_, String
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Anime, UserAnime

router = APIRouter(prefix="/anime", tags=["anime"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/top")
def get_top_anime(db: Session = Depends(get_db)):
    results = (
        db.query(Anime.anime_id, Anime.title, Anime.score, Anime.episodes)
        .order_by(func.nullif(cast(Anime.episodes, Integer), -1).desc())
        .limit(10)
        .all()
    )
    return [dict(row._mapping) for row in results]


@router.get("/popular")
def get_popular_anime(db: Session = Depends(get_db)):
    results = (
        db.query(Anime.genre, func.count(Anime.anime_id).label("view_count"))
        .join(UserAnime, UserAnime.anime_id == Anime.anime_id)
        .group_by(Anime.genre)
        .order_by(func.count(Anime.anime_id).desc())
        .limit(3)
    )
    return [dict(row._mapping) for row in results]


@router.post("/{anime_id}/episodes")
def update_anime_episodes(
    anime_id: str = Path(...),
    value: int = Query(1),
    db: Session = Depends(get_db)
):
    anime = db.query(Anime).filter(Anime.anime_id == anime_id).first()
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")

    anime.episodes = cast(cast(anime.episodes or '0', Integer) + value, String)
    db.commit()
    db.refresh(anime)

    return {
        "anime_id": anime.anime_id,
        "episodes": anime.episodes
    }
