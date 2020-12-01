from h3map.header.ab_reader import AbReader
from h3map.header.hota_reader import HotaReader
from h3map.header.roe_reader import RoeReader
from h3map.header.sod_reader import SodReader
from h3map.header.wog_reader import WogReader


supported_versions = {
    14: RoeReader,
    21: AbReader,
    28: SodReader,
    30: HotaReader,
    31: HotaReader,
    32: HotaReader,
    51: WogReader,
}
