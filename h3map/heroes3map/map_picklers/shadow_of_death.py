from h3map.heroes3map.map_picklers.win_loss_conditions import tag_cond, standard_win, \
    acquire_specific_artifact, accumulate_creatures, accumulate_resources, upgrade_specific_town, build_grail_structure, \
    defeat_specific_hero, capture_specific_town, defeat_specific_monster, flag_all_creatures, flag_all_mines, \
    transport_specific_artifact, standard_loss, lose_specific_town, lose_specific_hero, time_expires
from h3map.heroes3map.models import Header, PlayerInfo, AiType, FactionInfo, TownInfo, Hero, Metadata, TeamSetup, \
    CustomHeroInfo
from h3map.heroes3map.pypickler.picklers import Uint16, Bool
from h3map.heroes3map.pypickler.combinators import Uint32, Uint8, FixedList, \
    ArgWrap, kwrap, wrap, maybe, if_then, list_pp, string, altp
from h3map.heroes3map.transformations import _get_allowed_factions, _get_allowed_heroes


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
    player_infos=FixedList(
        kwrap(
            dict,
            can_human_play=Bool,
            can_computer_play=Bool,
            ai_type=kwrap(
                dict,
                ai_type=Bool,
                aggressiveness=Bool,
            ),
            faction_info=kwrap(
                dict,
                factions=wrap(
                    _get_allowed_factions,
                    _get_allowed_factions,
                    Uint16,
                ),
                is_faction_random=Bool,
            ),
            town_info=maybe(
                kwrap(
                    dict,
                    a=Bool,
                    b=Bool,
                    x=Uint8,
                    y=Uint8,
                    z=Uint8,
                )
            ),
            hero_properties=kwrap(
                dict,
                has_random_hero=Bool,
                custom=if_then(
                    lambda hid: True if hid != 255 else False,
                    kwrap(
                        dict,
                        customid=Uint8,
                        name=string()
                    )
                ),
            ),
            heroes=list_pp(
                wrap(lambda x: x[1], lambda x: (0, x, 0, 0), ArgWrap(Uint8, Uint8, Uint16, Uint8)),
                kwrap(dict, id=Uint8, name=string()))), 8),
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
