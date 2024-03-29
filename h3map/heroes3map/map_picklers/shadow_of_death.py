from h3map.heroes3map.map_picklers.shared import players
from h3map.heroes3map.map_picklers.win_loss_conditions import tag_cond, standard_win, \
    acquire_specific_artifact, accumulate_creatures, accumulate_resources, upgrade_specific_town, build_grail_structure, \
    defeat_specific_hero, capture_specific_town, defeat_specific_monster, flag_all_creatures, flag_all_mines, \
    transport_specific_artifact, standard_loss, lose_specific_town, lose_specific_hero, time_expires
from h3map.heroes3map.pypickler.combinators import Uint32, Uint8, FixedList, \
    kwrap, wrap, string, altp, Lift
from h3map.heroes3map.pypickler.picklers import Bool
from h3map.heroes3map.transformations import _get_allowed_heroes

shadow_of_death = kwrap(
    dict,
    metadata=kwrap(
        dict,
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
        transport_specific_artifact
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
