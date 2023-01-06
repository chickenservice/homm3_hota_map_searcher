from h3map.header.constants import heroes
from h3map.heroes3map.header.header_reader import Header, Metadata, PlayerInfo, Teams, AllowedHeroes, PlayerInfos, \
    AiTactic, FactionInfo, TownInfo, HeroProperties, HeroesBelongingToPlayers
from h3map.heroes3map.header.loss_conditions import LossConditionReader
from h3map.heroes3map.header.winning_conditions import WinningConditionReader


class WakeOfGods:
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
        return f"Wake of Gods\n\n{self.header}"


towns = ["castle",
         "rampart",
         "tower",
         "necropolis",
         "inferno",
         "dungeon",
         "stronghold",
         "fortress",
         "conflux",
         "neutral"]
