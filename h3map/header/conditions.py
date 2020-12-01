conditions = {
    0: "ARTIFACT",
    1: "GATHERTROOP",
    2: "GATHERRESOURCE",
    3: "BUILDCITY",
    4: "BUILDGRAIL",
    5: "BEATHERO",
    6: "CAPTURECITY",
    7: "BEATMONSTER",
    8: "TAKEDWELLINGS",
    9: "TAKEMINES",
    10: "TRANSPORTITEM",
    255: "WINSTANDARD",
}


def determine_loss_condition(parser):
    loss_conditions = [
        "LOSSCASTLE",
        "LOSSHERO",
        "TIMEEXPIRES",
        "LOSSSTANDARD",
    ]

    loss = parser.uint8()
    if 3 < loss <= 255:
        return loss_conditions[-1]

    if loss == 0 or loss == 1:
        parser.uint8()
        parser.uint8()
        parser.uint8()
    elif loss == 3:
        parser.uint16()
    elif loss > 3:
        raise ValueError("Loss condition not found: ", loss)

    return loss_conditions[loss]


def determine_winning_condition(parser):
    _conditions = [
        "ARTIFACT",
        "GATHERTROOP",
        "GATHERRESOURCE",
        "BUILDCITY",
        "BUILDGRAIL",
        "BEATHERO",
        "CAPTURECITY",
        "BEATMONSTER",
        "TAKEDWELLINGS",
        "TAKEMINES",
        "TRANSPORTITEM",
        "WINSTANDARD",
    ]

    _condition = parser.uint8()
    if 10 < _condition <= 255:
        return _conditions[-1]

    allow_normal_victory = parser.bool()
    applies_to_ai = parser.bool()

    if _condition == 0:
        parser.uint8()
        parser.skip(1)
    elif _condition == 1:
        parser.uint8()
        parser.skip(1)
        parser.uint32()
    elif _condition == 2:
        parser.uint8()
        parser.uint32()
    elif _condition == 3:
        parser.uint8()
        parser.uint8()
        parser.uint8()
        parser.uint8()
        parser.uint8()
    elif (4 <= _condition <= 7) or _condition == 10:
        parser.uint8()
        parser.uint8()
        parser.uint8()
    elif _condition > 10:
        raise ValueError("Winning condition not found: ", _condition)

    return _conditions[_condition]


def parse_victory_loss_condition(parser):
    return determine_winning_condition(parser), determine_loss_condition(parser)


