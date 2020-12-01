from h3map.header.map_reader import MapReader


class SodReader(MapReader):

    def __init__(self, parser, version=28):
        self.version = version
        self.parser = parser
        self.towns = towns
        super().__init__(parser)

    def __repr__(self):
        return "Shadow of Death"


towns = [
    "castle",
    "rampart",
    "tower",
    "necropolis",
    "inferno",
    "dungeon",
    "stronghold",
    "fortress",
    "conflux",
    "neutral",
]
