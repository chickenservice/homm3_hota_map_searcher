import abc
from typing import List

from h3map.header.models import Header, AcquireSpecificArtifact, TransportSpecificArtifact, FlagAllMines, \
    AccumulateCreatures, AccumulateResources, UpgradeSpecificTown, BuildGrailStructure, DefeatSpecificHero, \
    CaptureSpecificTown, DefeatSpecificMonster, FlagAllCreatures, Condition, TimeExpires, LoseSpecificHero, \
    LoseSpecificTown, StandardWinningCondition, StandardLossCondition


class FilterStrategy(abc.ABC):
    @abc.abstractmethod
    def filter(self, headers: List[Header]):
        raise NotImplemented("Please implement a concrete filter.")


class Filter:
    def __init__(self):
        self._filters = []

    def add_rule(self, strategy: FilterStrategy):
        self._filters.append(strategy)

    def clear(self):
        self._filters.clear()

    def filter(self, maps):
        result = []
        for f in self._filters:
            result += f.filter(maps)

        if not len(self._filters): return maps

        return result

    def apply(self, maps):
        result = []
        for f in self._filters:
            result += f.filter(maps)

        return result


class AndFilter(FilterStrategy):
    def __init__(self):
        self._filters = []

    def add(self, strategy: FilterStrategy):
        self._filters.append(strategy)

    def filter(self, maps):
        result = maps
        for f in self._filters:
            result = f.filter(result)

        return result

    def apply(self, maps):
        result = maps
        for f in self._filters:
            result = f.filter(result)

        return result


class TeamSizeFilter(FilterStrategy):
    def __init__(self, size):
        self.size = size

    def filter(self, headers: List[Header]):
        return [header for header in headers if self._has_teams(header)]

    def _has_teams(self, header):
        return header.teams.number_of_teams == self.size


class TeamPlayerNumberFilter(FilterStrategy):
    def __init__(self, players):
        self.players = players

    def filter(self, headers: List[Header]):
        return [header for header in headers if self._has_players(header)]

    def _has_players(self, header):
        from itertools import groupby
        return any([len(list(list(team)[1])) == self.players for team in groupby(sorted(header.teams.teams))])


class MapSizeFilter(FilterStrategy):
    _sizes = {
        "XL": 144,
        "L": 108,
        "M": 72,
        "S": 36,
    }

    def __init__(self, size):
        if size not in self._sizes:
            raise ValueError("Invalid map size specified.")

        self.size = self._sizes[size]

    def filter(self, headers: List[Header]):
        return [header for header in headers if self._has_size(header)]

    @classmethod
    def sizes(cls):
        return list(cls._sizes.keys())

    def _has_size(self, header):
        return header.metadata.properties.size == self.size


class WinLossConditionFilter(FilterStrategy):
    _conditions = {
        # Win conditions
        "Standard win": StandardWinningCondition,
        "Acquire artifact": AcquireSpecificArtifact,
        "Accumulate creatures": AccumulateCreatures,
        "Accumulate resources": AccumulateResources,
        "Upgrade town": UpgradeSpecificTown,
        "Build grail": BuildGrailStructure,
        "Defeat hero": DefeatSpecificHero,
        "Capture town": CaptureSpecificTown,
        "Defeat monster": DefeatSpecificMonster,
        "Flag creatures": FlagAllCreatures,
        "Flag mines": FlagAllMines,
        "Transport artifact": TransportSpecificArtifact,

        # Loss conditions
        "Standard loss": StandardLossCondition,
        "Lose town": LoseSpecificTown,
        "Lose hero": LoseSpecificHero,
        "Time expires": TimeExpires,
    }

    def __init__(self, condition):
        if condition not in self._conditions:
            raise ValueError("Invalid condition specified")

        self.condition = self._conditions[condition]

    def filter(self, headers: List[Header]):
        return [header for header in headers if any(self._has_condition(header))]

    def _has_condition(self, header):
        return [isinstance(c, self.condition) for c in header.conditions]
