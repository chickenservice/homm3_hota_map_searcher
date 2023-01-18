from h3map.heroes3map.pypickler.combinators import Sequ, wrap, kwrap, string, ArgWrap, FixedList, if_then, Lift
from h3map.heroes3map.pypickler.picklers import Uint8, Uint16, Bool


def ksequ(t, pa, kpb):
    return Sequ(
        lambda _: _,
        pa,
        lambda a: wrap(
            lambda b: t(**a, **b),
            lambda b: b,
            kpb(a)
        )
    )


test = ksequ(
    dict,
    kwrap(dict, unknown=Uint8, num_heroes=Uint8, unknown2=Uint16, unknown3=Uint8),
    lambda a: FixedList(kwrap(
        dict,
        id=Uint8,
        name=string()
    ), a.num_heroes)
)

test2 = ksequ(
    dict,
    kwrap(dict, has_random_hero=Bool, hid=Uint8),
    lambda a: kwrap(dict, customid=Uint8, name=string()) if a.hid != 255 else Lift(a)
)

heroes = Sequ(
    None,
    kwrap(dict, unknown=Uint8, num_heroes=Uint8, unknown2=Uint16, unknown3=Uint8),
    lambda info: wrap(
        lambda t: dict(**info, **t),
        lambda t: t,
        FixedList(kwrap(
            dict,
            id=Uint8,
            name=string()
        ), info.num_heroes)
    )
)

hp = Sequ(
    lambda _: _,
    kwrap(dict, has_random_hero=Bool, hid=Uint8),
    lambda a: wrap(
        lambda t: dict(**a, **t),
        lambda _: _,
        kwrap(dict, customid=Uint8, name=string()) if a.hid != 255 else Lift(a)
    )
)
