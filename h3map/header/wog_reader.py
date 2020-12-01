from h3map.header.map_reader import MapReader


class WogReader(MapReader):
    def __init__(self, parser, version=51):
        self.version = version
        self.towns = towns
        super().__init__(parser)

    def __repr__(self):
        return "Wake of Gods"


towns = ["castle",
         "rampart",
         "tower",
         "necropolis",
         "inferno",
         "dungeon",
         "stronghold",
         "fortress",
         "conflux",
         "neutral"]
