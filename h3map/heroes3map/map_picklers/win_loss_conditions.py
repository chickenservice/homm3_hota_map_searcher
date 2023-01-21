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

standard_loss = Lift(dict(name="Standard loss"))

lose_specific_town = kwrap(
    dict,
    name=Lift("Lose specific town"),
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

lose_specific_hero = kwrap(
    dict,
    name=Lift("Lose specific hero"),
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

time_expires = kwrap(
    dict,
    name=Lift("Time expires"),
    days=Uint16)

standard_win = Lift(dict(name="Standard win"))

acquire_specific_artifact = kwrap(
    dict,
    name=Lift("Acquire specific artifact"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    artifact_code=Uint8,
    skip=Uchar
)

accumulate_creatures = kwrap(
    dict,
    name=Lift("Accumulate creatures"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    unit_code=Uint8,
    skip=Uchar,
    amount=Uint32
)

accumulate_resources = kwrap(
    dict,
    name=Lift("Accumulate resources"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    resource_code=Uint8,
    amount=Uint32
)

upgrade_specific_town = kwrap(
    dict,
    name=Lift("Upgrade specific town"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
    hall_level=Uint8,
    castle_level=Uint8,
)

build_grail_structure = kwrap(
    dict,
    name=Lift("Build grail structure"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

defeat_specific_hero = kwrap(
    dict,
    name=Lift("Defeat specific hero"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

capture_specific_town = kwrap(
    dict,
    name=Lift("Capture specific town"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

defeat_specific_monster = kwrap(
    dict,
    name=Lift("Defeat specific monster"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

flag_all_creatures = kwrap(
    dict,
    name=Lift("Flag all creatures"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)

flag_all_mines = kwrap(
    dict,
    name=Lift("Flag all mines"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)

transport_specific_artifact = kwrap(
    dict,
    name=Lift("Transport specific artifact"),
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
