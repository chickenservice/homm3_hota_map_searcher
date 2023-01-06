from dataclasses import dataclass

from h3map.header.map_reader import MapReader
from h3map.header.models import MapProperties, Version


@dataclass
class HotaVersion(Version):
    minor: int
    patch: int


class HotaReader(MapReader):
    def __init__(self, parser, version=30):
        self.version = version
        self.parser = parser
        self.towns = towns
        super().__init__(parser)

    def read_version(self):
        minor = self.parser.uint32()
        patch = self.parser.uint8()

        return HotaVersion(self.version, minor, patch)

    def read_map_properties(self):
        any_players = self.parser.bool()
        _ = self.parser.uint8()
        height = self.parser.uint32()
        two_level = self.parser.bool()
        return MapProperties(any_players, height, two_level)

    def __repr__(self):
        return "Horn of the Abyss"


towns = ["castle",
         "rampart",
         "tower",
         "necropolis",
         "inferno",
         "dungeon",
         "stronghold",
         "fortress",
         "conflux",
         "cove",
         "neutral"]
