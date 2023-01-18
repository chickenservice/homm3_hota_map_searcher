from h3map.heroes3map.pypickler.combinators import Sequ, kwrap, string, FixedList, Lift, ksequ
from h3map.heroes3map.pypickler.picklers import Uint8, Uint16, Bool


heroes = Sequ(
    dict,
    kwrap(dict, unknown=Uint8, num_heroes=Uint8, unknown2=Uint16, unknown3=Uint8),
    lambda a: FixedList(kwrap(
        dict,
        id=Uint8,
        name=string()
    ), a["num_heroes"])
)

hero = ksequ(
    dict,
    kwrap(
        dict,
        has_random_hero=Bool,
        hid=Uint8
    ),
    lambda a: kwrap(
        dict,
        customid=Uint8,
        name=string()
    ) if a["hid"] != 255 else Lift(dict())
)
