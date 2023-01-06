from dataclasses import dataclass


@dataclass
class WinningCondition:
    allow_standard_win: bool
    ai_can_reach_it: bool


@dataclass
class StandardWinningCondition(WinningCondition):
    id: int = 0


@dataclass
class EliminateAllMonsters(WinningCondition):
    id: int = 1


@dataclass
class SurviveForCertainTime(WinningCondition):
    amount: int
    id: int = 1


@dataclass
class AcquireSpecificArtifact(WinningCondition):
    artifact_code: bool
    id: int = 1


@dataclass
class AccumulateCreatures(WinningCondition):
    unit_code: int
    amount: int
    id: int = 2


@dataclass
class AccumulateResources(WinningCondition):
    resource_code: int
    amount: int
    id: int = 3


@dataclass
class UpgradeSpecificTown(WinningCondition):
    x: int
    y: int
    z: int
    hall_level: int
    castle_level: int
    id: int = 4


@dataclass
class BuildGrailStructure(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 5


@dataclass
class DefeatSpecificHero(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 6


@dataclass
class CaptureSpecificTown(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 7


@dataclass
class DefeatSpecificMonster(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 8


@dataclass
class FlagAllCreatures(WinningCondition):
    id: int = 9


@dataclass
class FlagAllMines(WinningCondition):
    id: int = 10


@dataclass
class TransportSpecificArtifact(WinningCondition):
    artifact_code: int
    x: int
    y: int
    z: int
    id: int = 11
