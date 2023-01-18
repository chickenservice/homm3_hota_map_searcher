from h3map.header.models import AcquireSpecificArtifact, AccumulateCreatures
from h3map.heroes3map.map_picklers.win_loss_conditions import tag_cond, \
    transport_specific_artifact, flag_all_mines, flag_all_creatures, defeat_specific_monster, capture_specific_town, \
    defeat_specific_hero, build_grail_structure, upgrade_specific_town, accumulate_resources, \
    standard_win, standard_loss, lose_specific_town, lose_specific_hero, time_expires
from h3map.heroes3map.models import Header, PlayerInfo, AiType, FactionInfo, TownInfo, Hero, Metadata, TeamSetup, \
    CustomHeroInfo
from h3map.heroes3map.pypickler.picklers import Bool
from h3map.heroes3map.pypickler.combinators import Uint32, Uint8, FixedList, \
    kwrap, wrap, maybe, if_then, string, altp, Lift
from h3map.heroes3map.transformations import _get_allowed_factions, _get_allowed_heroes


acquire_specific_artifact = kwrap(
    dict,
    name=Lift("Acquire specific artifact"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    artifact_code=Uint8,
)

accumulate_creatures = kwrap(
    dict,
    name=Lift("Accumulate creatures"),
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    unit_code=Uint8,
    amount=Uint32
)

restoration_of_erathia = kwrap(
    dict,
    metadata=kwrap(
        dict,
        any_players=Bool,
        size=Uint32,
        two_level=Bool,
        name=string(),
        description=string(),
        difficulty=Uint8,
    ),
    player_infos=FixedList(
        kwrap(
            dict,
            can_human_play=Bool,
            can_computer_play=Bool,
            ai_type=kwrap(
                dict,
                ai_type=Bool,
            ),
            faction_info=kwrap(
                dict,
                factions=wrap(
                    _get_allowed_factions,
                    _get_allowed_factions,
                    Uint8,
                ),
                is_faction_random=Bool,
            ),
            town_info=maybe(
                kwrap(
                    dict,
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
            )
        ), 8),
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

