from abc import ABC

from h3map.header.models import StandardLossCondition, LoseSpecificTown, LoseSpecificHero, TimeExpires


class LossConditionReader(ABC):
    pass


class StandardLossConditionReader(LossConditionReader):
    def read(self):
        return StandardLossCondition(255)


class LoseSpecificTownReader(LossConditionReader):
    def __init__(self, parser):
        self.parser = parser

    def read(self):
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        return LoseSpecificTown(x, y, z)


class LoseSpecificHeroReader(LossConditionReader):
    def __init__(self, parser):
        self.parser = parser

    def read(self):
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        return LoseSpecificHero(x, y ,z)


class TimeExpiresReader(LossConditionReader):
    def __init__(self, parser):
        self.parser = parser

    def read(self):
        days = self.parser.uint16()
        return TimeExpires(days)


loss_condition_readers = {
    0: LoseSpecificTownReader,
    1: LoseSpecificHeroReader,
    2: TimeExpiresReader,
}
