from dataclasses import dataclass
from typing import List


ROE = 14




def get_allowed_factions(parser, version):
    factions = ["castle", "rampart", "tower", "necropolis", "inferno", "dungeon", "stronghold", "fortress", "conflux",
                "neutral"]
    total = parser.uint8()
    allowed = total
    if version != 14:
        allowed = total + parser.uint8() * 256
    else:
        total = max(total - 1, 0)
    return [faction for i, faction in enumerate(factions[:total]) if (allowed & (1 << i))]


def parse_player_info(parser, version):
    # INVALID = 0,
    # // HEX
    # DEC
    # ROE = 0x0e, // 14
    # AB = 0x15, // 21
    # SOD = 0x1c, // 28
    #
    # // HOTA = 0x1e...
    # 0x20 // 28...
    # 30
    # WOG = 0x33, // 51
    # VCMI = 0xF0
    players = []
    for player_num in range(0, 8):
        can_human_play = parser.bool()
        can_computer_play = parser.bool()
        if not (can_human_play or can_computer_play):
            if 28 <= version <= 32 or version == 51:
                parser.skip(13)
            elif version == 21:
                parser.skip(12)
            elif version == ROE:
                parser.skip(6)
            continue

        ai_tactic = parser.uint8()
        p7 = -1
        if 28 <= version <= 32 or version == 51:
            p7 = parser.uint8()
        allowed_factions = get_allowed_factions(parser, version)
        is_faction_random = parser.bool()
        has_main_town = parser.bool()

        if has_main_town:
            if version != ROE:
                parser.bool()
                parser.bool()
            parser.uint8()
            parser.uint8()
            parser.uint8()

        has_random_hero = parser.bool()
        main_custom_hero_id = parser.uint8()

        # TODO: Add proper handling for different ROE extensions:
        # https://github.com/potmdehex/homm3tools/blob/h3mlibhota/h3m/h3mlib/h3m_parsing/parse_players.c
        if version == ROE:
            if has_main_town and main_custom_hero_id != 255:
                _id = parser.uint8()
            elif not has_main_town and main_custom_hero_id != 255:
                _id = parser.uint8()
        elif main_custom_hero_id != 255:
            _id = parser.uint8()
            name = parser.string()

        _heroes = []
        if version != ROE:
            parser.uint8()
            hero_count = parser.uint8()
            parser.skip(3)

            for i in range(0, hero_count):
                _id = parser.uint8()
                name = parser.string()
                _heroes.append(Hero(_id, name))

        player = PlayerInfo(
            can_human_play,
            can_computer_play,
            ai_tactic,
            allowed_factions,
            p7,
            is_faction_random,
            has_main_town,
            has_random_hero,
            _heroes
        )

        players.append(player)

    return players
