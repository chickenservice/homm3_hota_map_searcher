from h3map.heroes3map.map_picklers.win_loss_conditions import winning_cond, loss_cond, tag_cond, standard_win, \
    acquire_specific_artifact, accumulate_creatures, accumulate_resources, upgrade_specific_town, build_grail_structure, \
    defeat_specific_hero, capture_specific_town, defeat_specific_monster, flag_all_creatures, flag_all_mines, \
    transport_specific_artifact, standard_loss, lose_specific_town, lose_specific_hero, time_expires
from h3map.heroes3map.models import Header, PlayerInfo, AiType, FactionInfo, TownInfo, Hero, Metadata, TeamSetup, \
    HeroInfo, CustomHeroInfo, HotaMetadata, HotaMetadataV2, HotaMetadataV1
from h3map.heroes3map.pypickler.picklers import Uint16, Bool, Uchar
from h3map.heroes3map.pypickler.combinators import Uint32, Uint8, FixedList, \
    ArgWrap, kwrap, wrap, maybe, if_then, list_pp, string, alt, Sequ, altp
from h3map.heroes3map.schema.transformations import _get_allowed_factions, _get_allowed_heroes
from h3map.heroes3map.winning_conditions import EliminateAllMonsters, SurviveForCertainTime

eliminate_all_monster = kwrap(
    EliminateAllMonsters,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
)

survive_for_certain_time = kwrap(
    SurviveForCertainTime,
    allow_standard_win=Bool,
    ai_can_reach_it=Bool,
    amount=Uint32
)


def _hota_minor_version(v):
    return 0 if v == 1 else 1


_hota_metadata_rev1 = kwrap(
    HotaMetadataV1,
    mirror=Bool,
    hota_arena=Uint8,
)

_hota_metadata_rev2 = kwrap(
    HotaMetadataV2,
    mirror=Bool,
    hota_arena=Uint8,
    terrain_count=Uint32,
)

_versions = [_hota_metadata_rev1, _hota_metadata_rev2]

horn_of_the_abyss = kwrap(
    Header,
    metadata=kwrap(
        Metadata,
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
    player_infos=FixedList(
        kwrap(
            PlayerInfo,
            can_human_play=Bool,
            can_computer_play=Bool,
            ai_type=kwrap(
                AiType,
                ai_type=Bool,
                aggressiveness=Bool,
            ),
            faction_info=kwrap(
                FactionInfo,
                factions=wrap(
                    _get_allowed_factions,
                    _get_allowed_factions,
                    Uint16,
                ),
                is_faction_random=Bool,
            ),
            town_info=maybe(
                kwrap(
                    TownInfo,
                    a=Bool,
                    b=Bool,
                    x=Uint8,
                    y=Uint8,
                    z=Uint8,
                )
            ),
            hero_properties=kwrap(
                CustomHeroInfo,
                has_random_hero=Bool,
                custom=if_then(
                    lambda hid: True if hid != 255 else False,
                    kwrap(
                        Hero,
                        customid=Uint8,
                        name=string()
                    )
                ),
            ),
            heroes=list_pp(
                wrap(lambda x: x[1], lambda x: (0, x, 0, 0), ArgWrap(Uint8, Uint8, Uint16, Uint8)),
                kwrap(Hero, id=Uint8, name=string()))), 8),
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
        TeamSetup,
        number_of_teams=Uint8,
        teams=FixedList(Uint8, 8),
    ),
    allowed_heroes=wrap(_get_allowed_heroes, _get_allowed_heroes, FixedList(Uint8, 20)))
