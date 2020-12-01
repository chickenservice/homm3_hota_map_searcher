def parse_header(parser):
    version = parser.uint32()
    if 30 <= version <= 32:
        parser.uint32()
        parser.uint8()

    any_players = parser.bool()
    if 30 <= version <= 32:
        parser.uint8()

    height = parser.uint32()
    two_level = parser.bool()
    name = parser.string()
    desc = parser.string()
    diff = parser.uint8()
    max_level = parser.uint8()

    print("Version: ", version)
    print("name: ", name)

    return version
