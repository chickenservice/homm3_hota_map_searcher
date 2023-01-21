from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from h3map.heroes3 import engine, Map, Player, Team

Session = sessionmaker(bind=engine)
session = Session()

maps = session.query(Map).join(Map.players).join(Player.team).group_by(Map.id).having(func.count(distinct(Player.team_id)) == 8).all()

all_maps = session.query(Map).all()
