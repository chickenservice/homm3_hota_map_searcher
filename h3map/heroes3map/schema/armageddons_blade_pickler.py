from h3map.heroes3map.models import Header, PlayerInfo, AiType, FactionInfo, TownInfo, Hero, Metadata, TeamSetup, \
    HeroInfo, CustomHeroInfo
from h3map.heroes3map.schema.to_remove_pypickler import KWrap, Bool, Uint32, String, Uint8, FixedList, Wrap, Uint16, Maybe, Alt, \
    Uchar, Lift, List, PList, Tuple, IfThen, AltP
from h3map.heroes3map.schema.transformations import _get_allowed_factions, _get_allowed_heroes
from h3map.heroes3map.loss_conditions import StandardLossCondition, LoseSpecificTown, LoseSpecificHero, TimeExpires
from h3map.heroes3map.winning_conditions import StandardWinningCondition, AcquireSpecificArtifact, AccumulateCreatures, \
    AccumulateResources, UpgradeSpecificTown, BuildGrailStructure, DefeatSpecificHero, CaptureSpecificTown, \
    DefeatSpecificMonster, FlagAllCreatures, FlagAllMines, TransportSpecificArtifact


def tag_cond(loss_condition_type):
    return 0 if loss_condition_type == 255 else loss_condition_type


loss_cond = AltP(tag_cond, lambda i: 0 if i == 255 else i,
                 [
                     Lift(StandardLossCondition),
                     KWrap(
                         LoseSpecificTown,
                         x=Uint8,
                         y=Uint8,
                         z=Uint8,
                     ),
                     KWrap(
                         LoseSpecificHero,
                         x=Uint8,
                         y=Uint8,
                         z=Uint8,
                     ),
                     KWrap(
                         TimeExpires,
                         days=Uint16
                     )])

winning_cond = AltP(tag_cond, lambda i: 0 if i == 255 else i,
                    [
                        Lift(StandardWinningCondition),
                        KWrap(
                            AcquireSpecificArtifact,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            artifact_code=Uint8,
                            skip=Uchar
                        ),
                        KWrap(
                            AccumulateCreatures,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            unit_code=Uint8,
                            skip=Uchar,
                            amount=Uint32
                        ),
                        KWrap(
                            AccumulateResources,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            resource_code=Uint8,
                            amount=Uint32
                        ),
                        KWrap(
                            UpgradeSpecificTown,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            x=Uint8,
                            y=Uint8,
                            z=Uint8,
                            hall_level=Uint8,
                            castle_level=Uint8,
                        ),
                        KWrap(
                            BuildGrailStructure,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            x=Uint8,
                            y=Uint8,
                            z=Uint8,
                        ),
                        KWrap(
                            DefeatSpecificHero,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            x=Uint8,
                            y=Uint8,
                            z=Uint8,
                        ),
                        KWrap(
                            CaptureSpecificTown,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            x=Uint8,
                            y=Uint8,
                            z=Uint8,
                        ),
                        KWrap(
                            DefeatSpecificMonster,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            x=Uint8,
                            y=Uint8,
                            z=Uint8,
                        ),
                        KWrap(
                            FlagAllCreatures,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                        ),
                        KWrap(
                            FlagAllMines,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                        ),
                        KWrap(
                            TransportSpecificArtifact,
                            allow_standard_win=Bool,
                            ai_can_reach_it=Bool,
                            x=Uint8,
                            y=Uint8,
                            z=Uint8,
                        )
                    ])

armageddons_blade = KWrap(
    Header,
    version=Uint32,
    metadata=KWrap(
        Metadata,
        any_players=Bool,
        size=Uint32,
        two_level=Bool,
        name=String(),
        description=String(),
        difficulty=Uint8,
        max_hero_level=Uint8,
    ),
    player_infos=FixedList(
        KWrap(
            PlayerInfo,
            can_human_play=Bool,
            can_computer_play=Bool,
            ai_type=KWrap(
                AiType,
                ai_type=Bool,
            ),
            faction_info=KWrap(
                FactionInfo,
                factions=Wrap(
                    _get_allowed_factions,
                    _get_allowed_factions,
                    Uint16,
                ),
                is_faction_random=Bool,
            ),
            town_info=Maybe(
                KWrap(
                    TownInfo,
                    a=Bool,
                    b=Bool,
                    x=Uint8,
                    y=Uint8,
                    z=Uint8,
                )
            ),
            hero_properties=KWrap(
                CustomHeroInfo,
                has_random_hero=Bool,
                custom=IfThen(
                    lambda hid: True if hid != 255 else False,
                    KWrap(
                        Hero,
                        customid=Uint8,
                        name=String()
                    )
                ),
            ),
            heroes=PList(
                Wrap(lambda x: x[1], lambda x: (0, x, 0, 0), Tuple([Uint8, Uint8, Uint16, Uint8])),
                KWrap(Hero, id=Uint8, name=String()))), 8),
    winning_condition=winning_cond,
    loss_condition=loss_cond,
    teams=KWrap(
        TeamSetup,
        number_of_teams=Uint8,
        teams=FixedList(Uint8, 8),
    ),
    allowed_heroes=Wrap(_get_allowed_heroes, _get_allowed_heroes, FixedList(Uint8, 20)))
