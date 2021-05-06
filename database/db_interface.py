import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from database.Battle import Battle, Base
from config.config import config

DB_PATH = os.path.join(config('PROJECT_PATH'), 'database')

engine = create_engine(
    f"sqlite:////{os.path.join(DB_PATH, 'battles.db')}")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_battles(battles):
    for battle in battles:
        session.merge(battle)

    session.commit()


def fetchall_short():
    return session.query(Battle.player_1_rating_final, Battle.player_2_rating_final, Battle.power, Battle.player_1).all()

def select_newest_date():
    return session.query(func.max(Battle.created_date)).first()[0]
