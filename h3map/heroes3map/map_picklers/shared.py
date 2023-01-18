from h3map.heroes3map.map_picklers.picklers import hero, heroes
from h3map.heroes3map.pypickler.combinators import FixedList, kwrap, wrap, maybe
from h3map.heroes3map.pypickler.picklers import Uint8, Uint16, Bool
from h3map.heroes3map.transformations import _get_allowed_factions

player = kwrap(
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
    hero_properties=hero,
    heroes=heroes
)

players = FixedList(player, 8)
