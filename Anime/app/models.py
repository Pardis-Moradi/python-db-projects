from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Anime(Base):
    __tablename__ = 'anime_list'

    anime_id = Column(Text, primary_key=True)
    title = Column(Text)
    title_english = Column(Text)
    title_japanese = Column(Text)
    episodes = Column(Text)
    score = Column(Text)
    scored_by = Column(Text)
    rank = Column(Text)
    popularity = Column(Text)
    members = Column(Text)
    favorites = Column(Text)
    rating = Column(Text)
    aired = Column(Text)
    aired_string = Column(Text)
    premiered = Column(Text)
    broadcast = Column(Text)
    producer = Column(Text)
    licensor = Column(Text)
    studio = Column(Text)
    genre = Column(Text)
    duration = Column(Text)
    type = Column(Text)
    source = Column(Text)
    opening_theme = Column(Text)
    ending_theme = Column(Text)
    related = Column(Text)
    status = Column(Text)
    image_url = Column(Text)
    background = Column(Text)
    airing = Column(Text)
    title_synonyms = Column(Text)


class User(Base):
    __tablename__ = 'user_list'

    user_id = Column(Text, primary_key=True)
    username = Column(Text)
    gender = Column(Text)
    birth_date = Column(Text)
    location = Column(Text)
    join_date = Column(Text)
    last_online = Column(Text)
    access_rank = Column(Text)
    stats_mean_score = Column(Text)
    stats_episodes = Column(Text)
    stats_rewatcher = Column(Text)
    user_days_spent_watching = Column(Text)
    user_watching = Column(Text)
    user_complete = Column(Text)
    user_onhold = Column(Text)
    user_dropped = Column(Text)
    user_plantowatch = Column(Text)


class UserAnime(Base):
    __tablename__ = 'user_anime_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text)
    anime_id = Column(Text)
    my_score = Column(Text)
    my_status = Column(Text)
    my_watched_episodes = Column(Text)
    my_start_date = Column(Text)
    my_finish_date = Column(Text)
    my_rewatching = Column(Text)
    my_rewatching_ep = Column(Text)
    my_last_updated = Column(Text)
    my_tags = Column(Text)