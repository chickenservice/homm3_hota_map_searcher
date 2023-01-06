from dataclasses import dataclass


@dataclass
class LossCondition:
    pass


@dataclass
class StandardLossCondition(LossCondition):
    number: int
    id: int = 0


@dataclass
class LoseSpecificTown(LossCondition):
    x: int
    y: int
    z: int
    id: int = 1


@dataclass
class LoseSpecificHero(LossCondition):
    x: int
    y: int
    z: int
    id: int = 2


@dataclass
class TimeExpires(LossCondition):
    days: int
    id: int = 3
