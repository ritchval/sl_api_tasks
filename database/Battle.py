import os
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from config.config import config

Base = declarative_base()

DB_PATH = os.path.join(config('PROJECT_PATH'), 'database')
class Battle(Base):
    __tablename__ = 'Battles'

    battle_queue_id_1 = Column(String)
    battle_queue_id_2 = Column(String)
    player_1_rating_initial = Column(Integer)
    player_2_rating_initial = Column(Integer)
    winner = Column(String)
    player_1_rating_final = Column(Integer)
    player_2_rating_final = Column(Integer)
    details = Column(Text)
    player_1 = Column(String)
    player_2 = Column(String)
    created_date = Column(String, primary_key=True)
    match_type = Column(String)
    mana_cap = Column(Integer)
    current_streak = Column(Integer)
    ruleset = Column(String)
    inactive = Column(String)
    settings = Column(String)
    block_num = Column(Integer)
    rshares = Column(Integer)
    dec_info = Column(String)
    leaderboard = Column(Integer)
    power = Column(Integer)


engine = create_engine(
    f"sqlite:////{os.path.join(DB_PATH, 'battles.db')}")

Base.metadata.create_all(engine)
