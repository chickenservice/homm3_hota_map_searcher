from h3map.header.constants import towns
from h3map.heroes3map._old.schema.heroes3schema import HeroPropertiesSchema
from h3map.heroes3map._old.schema.loss_conditions import LossCondition
from h3map.heroes3map.models import Header, PlayerInfo, AiType, FactionInfo, TownInfo, Metadata, TeamSetup
from h3map.heroes3map._old.schema.schema import Schema, Bool, Uint32, String, Uint8, Transform, If, MapRange
from h3map.heroes3map._old.schema.transformations import _get_allowed_heroes
from h3map.heroes3map._old.schema.winning_conditions import WinningCondition


def _get_allowed_factions(total):
    allowed = max(total - 1, 0)
    return [faction for i, faction in enumerate(towns[:total]) if (allowed & (1 << i))]


restoration_of_erathia = Schema(
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
    player_infos=MapRange(
        lambda p: p, 8,
        player=Schema(
            PlayerInfo,
            can_human_play=Bool,
            can_computer_play=Bool,
            ai_type=Schema(
                AiType,
                ai_type=Bool,
            ),
            faction_info=Transform(
                FactionInfo,
                _get_allowed_factions,
                total=Uint8,
                is_faction_random=Bool,
            ),
            town_info=If(
                TownInfo,
                Bool,
                x=Uint8,
                y=Uint8,
                z=Uint8,
            ),
            hero_properties=HeroPropertiesSchema(
                has_random_hero=Bool,
                main_custom_hero_id=Uint8,
                _id=Uint8,
                name=String,
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
