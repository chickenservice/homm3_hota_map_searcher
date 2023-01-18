from h3map.heroes3map.map_picklers.shared import players
from h3map.heroes3map.map_picklers.win_loss_conditions import tag_cond, standard_win, \
    acquire_specific_artifact, accumulate_creatures, accumulate_resources, upgrade_specific_town, build_grail_structure, \
    defeat_specific_hero, capture_specific_town, defeat_specific_monster, flag_all_creatures, flag_all_mines, \
    transport_specific_artifact, standard_loss, lose_specific_town, lose_specific_hero, time_expires
from h3map.heroes3map.pypickler.combinators import Uint32, Uint8, FixedList, \
    kwrap, wrap, string, Sequ, altp, Lift
from h3map.heroes3map.pypickler.picklers import Bool
from h3map.heroes3map.transformations import _get_allowed_heroes

eliminate_all_monster = kwrap(
    dict,
    name=Lift("Eliminate all monsters"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)

survive_for_certain_time = kwrap(
    dict,
    name=Lift("Survive for certain time"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    amount=Uint32
)


def _hota_minor_version(v):
    return 0 if v == 1 else 1


_hota_metadata_rev1 = kwrap(
    dict,
    mirror=Bool,
    hota_arena=Uint8,
)

_hota_metadata_rev2 = kwrap(
    dict,
    mirror=Bool,
    hota_arena=Uint8,
    terrain_count=Uint32,
)

_versions = [_hota_metadata_rev1, _hota_metadata_rev2]

horn_of_the_abyss = kwrap(
    dict,
    metadata=kwrap(
        dict,
        additional=Sequ(lambda v: _versions[_hota_minor_version(v)], Uint32,
                        lambda i: _versions[_hota_minor_version(i)]),
        any_players=Bool,
        size=Uint32,
        two_level=Bool,
        name=string(),
        description=string(),
        difficulty=Uint8,
        max_hero_level=Uint8,
    ),
    player_infos=players,
    winning_condition=altp(tag_cond, tag_cond, [
        standard_win,
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
        eliminate_all_monster,
        survive_for_certain_time
    ]),
    loss_condition=altp(tag_cond, tag_cond, [
        standard_loss,
        lose_specific_town,
        lose_specific_hero,
        time_expires
    ]),
    teams=kwrap(
        dict,
        number_of_teams=Uint8,
        teams=FixedList(Uint8, 8),
    ),
    allowed_heroes=wrap(_get_allowed_heroes, _get_allowed_heroes, FixedList(Uint8, 20)))
