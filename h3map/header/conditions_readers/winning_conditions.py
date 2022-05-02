from abc import ABC

from h3map.header.models import StandardWinningCondition, AcquireSpecificArtifact, DefeatSpecificHero, \
    CaptureSpecificTown, DefeatSpecificMonster, FlagAllCreatures, FlagAllMines, TransportSpecificArtifact, \
    AccumulateCreatures, AccumulateResources, BuildGrailStructure, UpgradeSpecificTown


class WinningConditionReader(ABC):
    def __init__(self, parser):
        self.parser = parser
        self.allow_standard_win = 0
        self.ai_can_reach_it = 1

    def read(self):
        self.allow_standard_win = self.parser.bool()
        self.ai_can_reach_it = self.parser.bool()


class StandardWinningConditionReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        return StandardWinningCondition(True, True)


class AcquireSpecificArtifactReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self, skip=0):
        super().read()
        artifact_code = self.parser.uint8()
        if skip > 0:
            self.parser.skip(skip)
        return AcquireSpecificArtifact(self.allow_standard_win, self.ai_can_reach_it, artifact_code)


class AccumulateCreaturesReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self, skip=0):
        super().read()
        unit_code = self.parser.uint8()
        if skip > 0:
            self.parser.skip(skip)
        amount = self.parser.uint32()
        return AccumulateCreatures(self.allow_standard_win, self.ai_can_reach_it, unit_code, amount)


class AccumulateResourcesReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        resource_code = self.parser.uint8()
        amount = self.parser.uint32()
        return AccumulateResources(self.allow_standard_win, self.ai_can_reach_it, resource_code, amount)


class UpgradeSpecificTownReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        hall_level = self.parser.uint8()
        castle_level = self.parser.uint8()
        return UpgradeSpecificTown(self.allow_standard_win, self.ai_can_reach_it, x, y, z, hall_level, castle_level)


class BuildGrailStructureReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        return BuildGrailStructure(self.allow_standard_win, self.ai_can_reach_it, x, y, z)


class DefeatSpecificHeroReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        return DefeatSpecificHero(self.allow_standard_win, self.ai_can_reach_it, x, y, z)


class CaptureSpecificTownReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        return CaptureSpecificTown(self.allow_standard_win, self.ai_can_reach_it, x, y, z)


class DefeatSpecificMonsterReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        return DefeatSpecificMonster(self.allow_standard_win, self.ai_can_reach_it, x, y, z)


class FlagAllCreaturesReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        return FlagAllCreatures(self.allow_standard_win, self.ai_can_reach_it)


class FlagAllMinesReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        return FlagAllMines(self.allow_standard_win, self.ai_can_reach_it)


class TransportSpecificArtifactReader(WinningConditionReader):
    def __init__(self, parser):
        super().__init__(parser)

    def read(self):
        super().read()
        artifact_code = self.parser.uint8()
        x = self.parser.uint8()
        y = self.parser.uint8()
        z = self.parser.uint8()
        return TransportSpecificArtifact(self.allow_standard_win, self.ai_can_reach_it, artifact_code, x, y, z)


winning_condition_readers = {
    0: AcquireSpecificArtifactReader,
    1: AccumulateCreaturesReader,
    2: AccumulateResourcesReader,
    3: UpgradeSpecificTownReader,
    4: BuildGrailStructureReader,
    5: DefeatSpecificHeroReader,
    6: CaptureSpecificTownReader,
    7: DefeatSpecificMonsterReader,
    8: FlagAllCreaturesReader,
    9: FlagAllMinesReader,
    10: TransportSpecificArtifactReader
}
