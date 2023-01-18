from h3map.heroes3map._old.schema.heroes3schema import HeroPropertiesSchema
from h3map.heroes3map._old.schema.loss_conditions import LossCondition
from h3map.heroes3map.models import Header, PlayerInfo, AiType, FactionInfo, TownInfo, Hero, Metadata, TeamSetup
from h3map.heroes3map._old.schema.schema import Schema, Bool, Uint32, String, Uint8, Uint16, Transform, If, Repeat, Select, Constant
from h3map.heroes3map._old.schema.transformations import _get_allowed_factions, _get_allowed_heroes
from h3map.heroes3map._old.schema.winning_conditions import WinningCondition

armageddons_blade = Schema(
    Header,
    metadata=Schema(
        Metadata,
        any_players=Bool,
        size=Uint32,
        two_level=Bool,
        name=String,
        description=String,
        difficulty=Uint8,
        max_hero_level=Uint8,
    ),
    player_infos=Repeat(
        Schema(
            PlayerInfo,
            can_human_play=Bool,
            can_computer_play=Bool,
            ai_type=Schema(
                AiType,
                ai_type=Bool,
            ),
            faction_info=Schema(
                FactionInfo,
                factions=Transform(
                    _get_allowed_factions,
                    allowed=Uint16,
                ),
                is_faction_random=Bool,
            ),
            town_info=Schema(
                    TownInfo,
                    has_main_town=If(Bool),
                    a=Bool,
                    b=Bool,
                    x=Uint8,
                    y=Uint8,
                    z=Uint8,
                ),
            hero_properties=HeroPropertiesSchema(
                has_random_hero=Bool,
                main_custom_hero_id=Uint8,
                id=Uint8,
                name=String,
            ),
            heroes=Repeat(
                Schema(
                    Hero,
                    id=Uint8,
                    name=String,
                ),
                Constant(0),
                Select(
                    "hero_count",
                    skip1=Uint8,
                    hero_count=Uint8,
                    skip2=Uint16,
                    skip3=Uint8,
                )
            )), Constant(0), Constant(8)),
    winning_condition=WinningCondition(
        condition=Uint8,
    ),
    loss_condition=LossCondition(
        condition=Uint8
    ),
    teams=Schema(
        TeamSetup,
        number_of_teams=Uint8,
        teams=Repeat(Uint8, Constant(0), Constant(8)),
    ),
    allowed_heroes=Transform(_get_allowed_heroes, heroes=Repeat(Uint8, Constant(0), Constant(20))))
