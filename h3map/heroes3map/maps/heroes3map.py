from h3map.heroes3map.maps.armageddons_blade import ArmageddonsBlade
from h3map.heroes3map.maps.horn_of_the_abyss import HornOfTheAbyss
from h3map.heroes3map.maps.restoration_of_erathia import RestorationOfErathia
from h3map.heroes3map.maps.shadow_of_death import ShadowOfDeath
from h3map.heroes3map.maps.wake_of_gods import WakeOfGods


class Heroes3Map:
    def __init__(self, stream):
        self._stream = stream
        self._map_versions = {
            14: RestorationOfErathia,
            21: ArmageddonsBlade,
            28: ShadowOfDeath,
            30: ShadowOfDeath,
            31: HornOfTheAbyss,
            32: HornOfTheAbyss,
            51: WakeOfGods,
        }
        self._read()

    def _read(self):
        self.version = self._stream.uint32()
        self.map = self._map_versions[self.version](self._stream)

    def __repr__(self):
        return f"Version: {self.version}\n{self.map}"
