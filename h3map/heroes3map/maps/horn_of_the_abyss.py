from h3map.header.constants import heroes
from h3map.heroes3map.header.header_reader import Header, PlayerInfo, Teams, AllowedHeroes, PlayerInfos, \
    AiTactic, FactionInfo, TownInfo, HeroProperties, HeroesBelongingToPlayers, _decode
from h3map.heroes3map.header.loss_conditions import LossConditionReader
from h3map.heroes3map.header.winning_conditions import WinningConditionReader


class Metadata:
    def __init__(self, stream):
        self.patch = None
        self.minor = None
        self.diff = None
        self.max_level = None
        self.description = None
        self.name = None
        self.two_level = None
        self.height = None
        self.any_players = None
        self._stream = stream

    def read(self):
        self.minor = self._stream.uint32()
        self.patch = self._stream.uint8()

        self.any_players = self._stream.bool()
        _ = self._stream.uint8()
        self.height = self._stream.uint32()
        self.two_level = self._stream.bool()
        self.name = _decode(self._stream.string())
        self.description = _decode(self._stream.string())
        self.diff = self._stream.uint8()
        self.max_level = self._stream.uint8()

    def __repr__(self):
        return f"Any players: {self.any_players}\n" \
               f"Size: {self.height}\n" \
               f"Two levels: {self.two_level}\n" \
               f"Name: {self.name}\n" \
               f"Description: {self.description}\n" \
               f"Difficulty: {self.diff}\n" \
               f"Level cap: {self.max_level}\n"


class HornOfTheAbyss:
    def __init__(self, stream):
        self._stream = stream
        self._read()

    def _read(self):
        self.header = Header(
            metadata=Metadata(self._stream),
            player_infos=PlayerInfos(
                player_info=[PlayerInfo(
                    self._stream, i,
                    ai_tactic=AiTactic(self._stream),
                    faction_info=FactionInfo(self._stream, towns=towns),
                    town_info=TownInfo(self._stream),
                    hero_props=HeroProperties(self._stream),
                    heroes=HeroesBelongingToPlayers(self._stream)
                ) for i in range(1, 9)]),
            winning_condition=WinningConditionReader(self._stream),
            loss_condition=LossConditionReader(self._stream),
            teams=Teams(self._stream),
            allowed_heroes=AllowedHeroes(self._stream, heroes=heroes),
        )

        self.header.read()

    def __repr__(self):
        return f"Horn of the Abyss\n\n{self.header}"


towns = ["castle",
         "rampart",
         "tower",
         "necropolis",
         "inferno",
         "dungeon",
         "stronghold",
         "fortress",
         "conflux",
         "cove",
         "neutral"]
