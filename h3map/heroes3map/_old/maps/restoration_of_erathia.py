from h3map.header.constants import heroes
from h3map.heroes3map._old.header.header_reader import Header, Metadata, Teams, AllowedHeroes, PlayerInfos, \
    HeroProperties
from h3map.heroes3map._old.header.loss_conditions import LossConditionReader
from h3map.heroes3map._old.header.winning_conditions import WinningConditionReader


class PlayerInfo:
    def __init__(self, stream, number, ai_tactic=None, faction_info=None, town_info=None, hero_props=None, heroes=None):
        self.can_computer_play = None
        self.can_human_play = None
        self.parser = stream
        self.number = number
        self.ai_tactic = ai_tactic
        self.faction_info = faction_info
        self.town_info = town_info
        self.hero_properties = hero_props

    def read(self):
        self.can_human_play = self.parser.bool()
        self.can_computer_play = self.parser.bool()
        if self._not_playable():
            self.parser.skip(6)
        else:
            self.ai_tactic.read()
            self.faction_info.read()
            self.town_info.read()
            self.hero_properties.read()

    def _not_playable(self):
        return not (self.can_human_play or self.can_computer_play)

    def __repr__(self):
        return f"Player {self.number}\nAI: {self.ai_tactic}\nFactions:{self.faction_info}\nTowns:{self.town_info}\nHero props:{self.hero_properties}\n\n"


class AiTactic:
    def __init__(self, stream):
        self.ai_tactic = None
        self.parser = stream

    def read(self):
        self.ai_tactic = self.parser.uint8()

    def __repr__(self):
        return f"{self.ai_tactic}"


class FactionInfo:
    def __init__(self, stream, factions=None):
        self.is_faction_random = None
        self.allowed_factions = None
        self.allowed = None
        self.total = None
        self.parser = stream
        self._towns = factions if factions else []

    def read(self):
        self.total = self.parser.uint8()
        self.allowed = max(self.total - 1, 0)
        self.allowed_factions = self._get_allowed_factions()
        self.is_faction_random = self.parser.bool()

    def _get_allowed_factions(self):
        return [faction for i, faction in enumerate(self._towns[:self.total]) if (self.allowed & (1 << i))]

    def __repr__(self):
        return "\n".join(self.allowed_factions)


class TownInfo:
    def __init__(self, stream):
        self.z = None
        self.y = None
        self.x = None
        self.has_main_town = None
        self.parser = stream

    def read(self):
        self.has_main_town = self.parser.bool()
        if self.has_main_town:
            self.x = self.parser.uint8()
            self.y = self.parser.uint8()
            self.z = self.parser.uint8()

    def __repr__(self):
        return f"Has main town: {self.has_main_town}"


class RestorationOfErathia:
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
                    faction_info=FactionInfo(self._stream, factions=towns),
                    town_info=TownInfo(self._stream),
                    hero_props=HeroProperties(self._stream),
                ) for i in range(1, 9)]),
            winning_condition=WinningConditionReader(self._stream),
            loss_condition=LossConditionReader(self._stream),
            teams=Teams(self._stream),
            allowed_heroes=AllowedHeroes(self._stream, heroes=heroes),
        )

        self.header.read()

    def __repr__(self):
        return f"Restoration of Erathia\n\n{self.header}"


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
