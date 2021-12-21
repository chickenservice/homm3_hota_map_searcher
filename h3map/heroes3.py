from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table, UniqueConstraint, \
    CheckConstraint, MetaData
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///' + str(Path.home()) + '/Projects/Homm3_Hota_Map_Searcher/.cache/h3map.db')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata_obj = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata_obj)

player_town = Table('player_town', Base.metadata,
                    Column('player_id', ForeignKey('player.id'), primary_key=True),
                    Column('town_id', ForeignKey('town.id'), primary_key=True),
                    )


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    maps_location = Column(String)


class Map(Base):
    __tablename__ = 'map'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    any_players = Column(Boolean)

    version_id = Column(Integer, ForeignKey("version.id"))
    version = relationship("Version")

    map_size_id = Column(Integer, ForeignKey("map_size.id"))
    map_size = relationship("MapSize")

    difficulty_id = Column(Integer, ForeignKey("difficulty.id"))
    difficulty = relationship("Difficulty")

    players = relationship("Player")

    winning_condition_id = Column(Integer, ForeignKey("winning_condition.id"))
    winning_condition = relationship("WinningCondition")

    loss_condition_id = Column(Integer, ForeignKey("loss_condition.id"))
    loss_condition = relationship("LossCondition")

    def __repr__(self):
        return "<Map(name=%s, version=%s, map_size=%s)" % (self.name, self.version, self.map_size)


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)

    map_id = Column(Integer, ForeignKey("map.id"))

    player_color_id = Column(Integer, ForeignKey("player_color.id"))
    player_color = relationship("PlayerColor")

    towns = relationship("Town", secondary=player_town)

    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("Team")

    def __repr__(self):
        return "<Player(name=%s, team=%s, color=%s)>" % (self.name, self.team, self.color)


class Version(Base):
    __tablename__ = 'version'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    version = Column(Integer)

    def __repr__(self):
        return "<Version(name=%s, version=%s)>" % (self.name, self.version)


class Difficulty(Base):
    __tablename__ = 'difficulty'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    difficulty = Column(Integer)

    def __repr__(self):
        return "<Difficulty(name=%s, difficulty=%s)>" % (self.name, self.difficulty)


class MapSize(Base):
    __tablename__ = 'map_size'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(Integer)

    def __repr__(self):
        return "<MapSize(name=%s, difficulty=%s)>" % (self.name, self.size)


class PlayerColor(Base):
    __tablename__ = 'player_color'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<PlayerColor(name=%s)>" % self.name


class Town(Base):
    __tablename__ = 'town'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Town(name=%s)>" % self.name


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Team(name=%s)>" % self.name


class WinningCondition(Base):
    __tablename__ = 'winning_condition'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<WinningCondition(name=%s)>" % self.name


class LossCondition(Base):
    __tablename__ = 'loss_condition'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<LossCondition(name=%s)>" % self.name
