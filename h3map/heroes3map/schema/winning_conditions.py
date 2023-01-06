from h3map.heroes3map.winning_conditions import StandardWinningCondition, AcquireSpecificArtifact, AccumulateCreatures, \
    AccumulateResources, UpgradeSpecificTown, BuildGrailStructure, DefeatSpecificHero, CaptureSpecificTown, \
    DefeatSpecificMonster, FlagAllCreatures, FlagAllMines, TransportSpecificArtifact
from h3map.heroes3map.schema.schema import Uint8, Schema, Uchar, Uint32, Bool


class WinningCondition(Schema):
    def __init__(self, winning_conditions=None, **kwargs):
        super().__init__(None, **kwargs)
        self._winning_conditions = _winning_condition_readers

    def __call__(self, stream, **kwargs):
        winning_condition_type = self._attrs["condition"](stream)
        if winning_condition_type == 255:
            return StandardWinningCondition(True, True)
        else:
            return self._winning_conditions[winning_condition_type](stream)


acquire_specific_artifact = Schema(
    AcquireSpecificArtifact,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    artifact_code=Uint8,
    skip=Uchar
)

accumulate_creatures = Schema(
    AccumulateCreatures,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    unit_code=Uint8,
    skip=Uchar,
    amount=Uint32
)

accumulate_resources = Schema(
    AccumulateResources,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    resource_code=Uint8,
    amount=Uint32
)


upgrade_specific_town = Schema(
    UpgradeSpecificTown,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
    hall_level=Uint8,
    castle_level=Uint8,
)


build_grail_structure = Schema(
    BuildGrailStructure,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)


defeat_specific_hero = Schema(
    DefeatSpecificHero,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)


capture_specific_town = Schema(
    CaptureSpecificTown,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)


defeat_specific_monster = Schema(
    DefeatSpecificMonster,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)


flag_all_creatures = Schema(
    FlagAllCreatures,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)


flag_all_mines = Schema(
    FlagAllMines,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)


transport_specific_artifact = Schema(
    TransportSpecificArtifact,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)


_winning_condition_readers = [
    acquire_specific_artifact,
    accumulate_creatures,
    accumulate_resources,
    upgrade_specific_town,
    build_grail_structure,
    defeat_specific_hero,
    capture_specific_town,
    defeat_specific_monster,
    flag_all_creatures,
    flag_all_mines,
    transport_specific_artifact,
]
