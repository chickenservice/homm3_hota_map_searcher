from dataclasses import dataclass

from header.RoeReader import RoeReader
from header.AbReader import AbReader
from header.SodReader import SodReader
from header.HotaReader import HotaReader
from header.WogReader import WogReader

from header.models.nodes import Metadata, PlayerInfo, Teams, AllowedHeroes


@dataclass
class Header:
    metadata: Metadata
    player_info: PlayerInfo
    teams: Teams
    allowed_heroes: AllowedHeroes


class Reader:
    supported_versions = {
        14: RoeReader,
        21: AbReader,
        28: SodReader,
        30: HotaReader,
        31: HotaReader,
        32: HotaReader,
        51: WogReader,
    }

    def __init__(self, parser):
        self.parser = parser

    def read(self):
        version = self.parser.uint32()
        reader = self._get_reader(version)

        metadata, player_info, teams, allowed_heroes = reader.read()

        return Header(metadata, player_info, teams, allowed_heroes)

    def _get_reader(self, version):
        return self.supported_versions[version](self.parser, version=version)
