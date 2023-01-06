from h3map.header.constants import towns, heroes


def _get_allowed_factions(allowed):
    return [faction for i, faction in enumerate(towns) if (allowed & (1 << i))]


def _get_allowed_heroes(actually_allowed):
    number_of_heroes = len(heroes)
    negate = False
    allowed_heroes = [True] * number_of_heroes
    for byte in range(0, 20):
        allowed = actually_allowed[byte]
        for bit in range(0, 8):
            if byte * 8 + bit < number_of_heroes:
                flag = allowed & (1 << bit)
                if (negate & flag) or ((not negate) & (not flag)):
                    allowed_heroes.insert(byte * 8 + bit, False)

    return [h for i, h in enumerate(heroes) if allowed_heroes[i]]


