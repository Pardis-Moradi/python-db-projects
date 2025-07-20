from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from sqlalchemy import cast, Integer, Float, and_
from app.database import SessionLocal
from app.models import User, UserAnime, Anime

router = APIRouter(prefix="/users", tags=["users"])

UAL1 = aliased(UserAnime)
UAL2 = aliased(UserAnime)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/top")
def get_top_users(
    page: int = Query(1, ge=1),
    offset: int = Query(10, ge=1),
    year: int = Query(2017),
    gender: str = Query("Female"),
    db: Session = Depends(get_db)
):
    results = (
        db.query(User.username, User.stats_mean_score)
        .filter(cast(func.nullif(User.stats_mean_score, '0.0'), Float) > 8.0)
        .filter(cast(func.substr(User.join_date, 1, 4), Integer) > year)
        .filter(User.gender == gender)
        .order_by(cast(func.nullif(User.stats_mean_score, '0.0'), Float).desc())
        .offset((page - 1) * offset)
        .limit(offset)
    )

    return [dict(row._mapping) for row in results]


@router.get("/{username}/watched")
def get_user_watched(username: str, count: int = Query(10), db: Session = Depends(get_db)):
    results = (
        db.query(Anime.anime_id, Anime.title, UserAnime.my_score, UserAnime.my_watched_episodes)
        .filter(UserAnime.username == username)
        .filter(Anime.anime_id == UserAnime.anime_id)
        .order_by(cast(func.nullif(UserAnime.my_score, '0'), Integer))
        .limit(count)
    )
    return [dict(row._mapping) for row in results]


@router.get("/active/{year}")
def get_active_users(year: int, db: Session = Depends(get_db)):
    results = (
        db.query(User.username, User.user_days_spent_watching)
        .filter(cast(func.substr(User.join_date, 1, 4), Integer) == year)
        .order_by(cast(func.nullif(User.user_days_spent_watching, '0.0'), Float).desc())
        .limit(5)
    )
    return [dict(row._mapping) for row in results]


@router.get("/{username}/similars")
def get_similar_users(username: str, db: Session = Depends(get_db)):
    results = (
        db.query(UAL2.username, func.count(UAL1.anime_id).label("common_anime_count"))
        .filter(UAL1.username == username)
        .join(UAL2, and_(UAL1.anime_id == UAL2.anime_id, UAL2.username != username))
        .group_by(UAL2.username)
    )
    return [dict(row._mapping) for row in results]

