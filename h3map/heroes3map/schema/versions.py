from h3map.heroes3map.schema.armageddons_blade import armageddons_blade
from h3map.heroes3map.schema.schema import Uint32

versions = {
#    14: restoration_of_erathia,
    21: armageddons_blade,
#    28: shadow_of_death,
#    30: horn_of_the_abyss,
#    31: horn_of_the_abyss,
#    32: horn_of_the_abyss,
#    51: wake_of_gods,
}


class H3mSchema:
    def __init__(self, version):
        self._version = version

    def __call__(self, stream, **kwargs):
        return versions[self._version(stream)](stream)


heroes3map = H3mSchema(
    version=Uint32,
)
