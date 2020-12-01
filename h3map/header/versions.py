from h3map.header.AbReader import AbReader
from h3map.header.HotaReader import HotaReader
from h3map.header.RoeReader import RoeReader
from h3map.header.SodReader import SodReader
from h3map.header.WogReader import WogReader


supported_versions = {
    14: RoeReader,
    21: AbReader,
    28: SodReader,
    30: HotaReader,
    31: HotaReader,
    32: HotaReader,
    51: WogReader,
}
