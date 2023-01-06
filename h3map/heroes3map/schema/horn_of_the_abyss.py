from h3map.heroes3map.schema.heroes3schema import HeroPropertiesSchema
from h3map.heroes3map.schema.loss_conditions import LossCondition
from h3map.heroes3map.models import Header, PlayerInfo, AiType, FactionInfo, TownInfo, Hero, Metadata, TeamSetup
from h3map.heroes3map.schema.schema import Schema, Bool, Uint32, String, Uint8, Uint16, Transform, If, Map, MapRange
from h3map.heroes3map.schema.transformations import _get_allowed_factions, _get_allowed_heroes
from h3map.heroes3map.schema.winning_conditions import WinningCondition


horn_of_the_abyss: Schema = Schema(
    Header,
    metadata=Schema(
        Metadata,
        minor=Uint32,
        patch=Uint8,
        any_players=Bool,
        _=Uint8,
        size=Uint32,
        two_level=Bool,
        name=String,
        description=String,
        difficulty=Uint8,
        max_hero_level=Uint8,
    ),
    player_infos=MapRange(
        lambda p: p, 8,
        player=Schema(
            PlayerInfo,
            can_human_play=Bool,
            can_computer_play=Bool,
            ai_type=Schema(
                AiType,
                ai_type=Bool,
                aggressiveness=Uint8
            ),
            faction_info=Transform(
                FactionInfo,
                _get_allowed_factions,
                total=Uint8,
                allowed=Uint8,
                is_faction_random=Bool,
            ),
            town_info=If(
                TownInfo,
                Bool,
                a=Bool,
                b=Bool,
                x=Uint8,
                y=Uint8,
                z=Uint8,
            ),
            hero_properties=HeroPropertiesSchema(
                has_random_hero=Bool,
                main_custom_hero_id=Uint8,
                _id=Uint8,
                name=String,
            ),
            heroes=Map(
                Schema(
                    Hero,
                    _id=Uint8,
                    name=String,
                ),
                "hero_count",
                skip1=Uint8,
                hero_count=Uint8,
                skip2=Uint16,
                skip3=Uint8,
            ))),
    winning_condition=WinningCondition(
        condition=Uint8,
    ),
    loss_condition=LossCondition(
        condition=Uint8
    ),
    teams=Schema(
        TeamSetup,
        number_of_teams=Uint8,
        teams=MapRange(
            lambda x: x,
            8,
            team=Uint8),
    ),
    allowed_heroes=MapRange(_get_allowed_heroes, 20, allowed=Uint8))
