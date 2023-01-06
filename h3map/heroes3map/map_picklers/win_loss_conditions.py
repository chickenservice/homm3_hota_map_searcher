from h3map.heroes3map.loss_conditions import StandardLossCondition, LoseSpecificTown, LoseSpecificHero, TimeExpires
from h3map.heroes3map.pypickler.combinators import altp, Lift, kwrap
from h3map.heroes3map.pypickler.picklers import Uint8, Uint16, Bool, Uchar, Uint32
from h3map.heroes3map.winning_conditions import StandardWinningCondition, AcquireSpecificArtifact, AccumulateCreatures, \
    AccumulateResources, UpgradeSpecificTown, BuildGrailStructure, DefeatSpecificHero, CaptureSpecificTown, \
    DefeatSpecificMonster, FlagAllCreatures, FlagAllMines, TransportSpecificArtifact


def tag_cond(loss_condition_type):
    return 0 if loss_condition_type == 255 else loss_condition_type + 1


loss_cond = altp(tag_cond, tag_cond,
                 [
                 ])

standard_loss = Lift(StandardLossCondition)

lose_specific_town = kwrap(
    LoseSpecificTown,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

lose_specific_hero = kwrap(
    LoseSpecificHero,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

time_expires = kwrap(
    TimeExpires,
    days=Uint16)

standard_win = Lift(StandardWinningCondition)

acquire_specific_artifact = kwrap(
    AcquireSpecificArtifact,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    artifact_code=Uint8,
    skip=Uchar
)

accumulate_creatures = kwrap(
    AccumulateCreatures,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    unit_code=Uint8,
    skip=Uchar,
    amount=Uint32
)

accumulate_resources = kwrap(
    AccumulateResources,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    resource_code=Uint8,
    amount=Uint32
)

upgrade_specific_town = kwrap(
    UpgradeSpecificTown,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
    hall_level=Uint8,
    castle_level=Uint8,
)

build_grail_structure = kwrap(
    BuildGrailStructure,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

defeat_specific_hero = kwrap(
    DefeatSpecificHero,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

capture_specific_town = kwrap(
    CaptureSpecificTown,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

defeat_specific_monster = kwrap(
    DefeatSpecificMonster,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

flag_all_creatures = kwrap(
    FlagAllCreatures,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)

flag_all_mines = kwrap(
    FlagAllMines,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)

transport_specific_artifact = kwrap(
    TransportSpecificArtifact,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    artifact_code=Uint8,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

winning_cond = altp(tag_cond, tag_cond,
                    [
                    ])
