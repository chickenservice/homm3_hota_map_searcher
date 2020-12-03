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


class HeaderFilter:
    def __init__(self):
        self.filters = []

    def has_team_size(self, size):
        team_size = TeamSizeFilter(size)
        self._add_filter(team_size)

    def has_map_size(self, size):
        map_size = MapSizeFilter(size)
        self._add_filter(map_size)

    def alliances_possible(self):
        team_size = TeamSizeFilter(2)
        self._add_filter(team_size)

    def has_win_or_loss_condition(self, condition):
        winning_condition = WinLossConditionFilter(condition)
        self._add_filter(winning_condition)

    def apply(self, headers: List[Header]):
        _headers = headers
        for _filter in self.filters:
            _headers = _filter.filter(_headers)

        return _headers

    def _add_filter(self, strategy: FilterStrategy):
        self.filters.append(strategy)


class TeamSizeFilter(FilterStrategy):
    def __init__(self, size):
        self.size = size

    def filter(self, headers: List[Header]):
        return [header for header in headers if self._has_teams(header)]

    def _has_teams(self, header):
        return header.teams.number_of_teams == self.size


class MapSizeFilter(FilterStrategy):
    _sizes = {
        "XL": 144,
        "L": 72,
        "M": 36,
        "S": 18,
    }

    def __init__(self, size):
        if size not in self._sizes:
            raise ValueError("Invalid map size specified.")

        self.size = self._sizes[size]

    def filter(self, headers: List[Header]):
        return [header for header in headers if self._has_size(header)]

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
