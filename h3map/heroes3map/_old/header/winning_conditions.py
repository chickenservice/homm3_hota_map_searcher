class WinningConditionReader:
    def __init__(self, parser, winning_conditions=None):
        self.winning_condition = None
        self.ai_can_reach_it = None
        self.allow_standard_win = None
        self.winning_condition_type = None
        self.parser = parser
        self._winning_conditions = _winning_condition_readers

    def read(self):
        self.winning_condition_type = self.parser.uint8()
        if self.winning_condition_type == 255:
            self.winning_condition = StandardWinningConditionReader(self.parser)
        else:
            self.allow_standard_win = self.parser.bool()
            self.ai_can_reach_it = self.parser.bool()
            self.winning_condition = self._winning_conditions[self.winning_condition_type](self.parser)

    def __str__(self):
        return str(self.winning_condition)


class StandardWinningConditionReader:
    def __init__(self, parser):
        pass

    def __str__(self):
        return "Standard Winning Condition"


class AcquireSpecificArtifactReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.artifact_code = self.parser.uint8()
        self.parser.skip(1)

    def __str__(self):
        return "Acquire specific artifact"


class AccumulateCreaturesReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.unit_code = self.parser.uint8()
        self.parser.skip(1)
        self.amount = self.parser.uint32()

    def __str__(self):
        return "Accumulate creatures"


class AccumulateResourcesReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.resource_code = self.parser.uint8()
        self.amount = self.parser.uint32()

    def __str__(self):
        return "Accumulate resources"


class UpgradeSpecificTownReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()
        self.hall_level = self.parser.uint8()
        self.castle_level = self.parser.uint8()

    def __str__(self):
        return "Upgrade specific town"


class BuildGrailStructureReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()

    def __str__(self):
        return "Build grail structure"


class DefeatSpecificHeroReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()

    def __str__(self):
        return "Defeat specific hero"


class CaptureSpecificTownReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()

    def __str__(self):
        return "Capture specific town"


class DefeatSpecificMonsterReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()

    def __str__(self):
        return "Defeat specific monster"


class FlagAllCreaturesReader:
    def __init__(self, parser):
        pass

    def __str__(self):
        return "Flag all creatures"


class FlagAllMinesReader:
    def __init__(self, parser):
        pass

    def __str__(self):
        return "Flag all mines"


class TransportSpecificArtifactReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def __str__(self):
        return "Transport specific artifact"

    def _read(self):
        self.artifact_code = self.parser.uint8()
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()


_winning_condition_readers = [
    AcquireSpecificArtifactReader,
    AccumulateCreaturesReader,
    AccumulateResourcesReader,
    UpgradeSpecificTownReader,
    BuildGrailStructureReader,
    DefeatSpecificHeroReader,
    CaptureSpecificTownReader,
    DefeatSpecificMonsterReader,
    FlagAllCreaturesReader,
    FlagAllMinesReader,
    TransportSpecificArtifactReader,
]
