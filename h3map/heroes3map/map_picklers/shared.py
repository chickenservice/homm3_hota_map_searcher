from h3map.heroes3map.pypickler.combinators import FixedList, kwrap, wrap, string, ArgWrap, if_then, list_pp, maybe
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
            kwrap(dict, id=Uint8, name=string())))

players = FixedList(player, 8)
