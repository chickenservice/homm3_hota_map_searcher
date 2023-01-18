from h3map.heroes3map.map_picklers.armageddons_blade import armageddons_blade
from h3map.heroes3map.map_picklers.horn_of_the_abyss import horn_of_the_abyss
from h3map.heroes3map.map_picklers.restoration_of_erathia import restoration_of_erathia
from h3map.heroes3map.map_picklers.shadow_of_death import shadow_of_death
from h3map.heroes3map.map_picklers.wake_of_gods import wake_of_gods
from h3map.heroes3map.pypickler.combinators import Sequ
from h3map.heroes3map.pypickler.picklers import Uint32

maps = {
    14: 0,  # RestorationOfErathia,
    21: 1,  # ArmageddonsBlade,
    28: 2,  # ShadowOfDeath,
    30: 2,  # HornOfTheAbyss,
    31: 3,  # HornOfTheAbyss,
    32: 3,  # HornOfTheAbyss,
    51: 4,  # WakeOfGods,
}

p = [
    restoration_of_erathia,
    armageddons_blade,
    shadow_of_death,
    horn_of_the_abyss,
    wake_of_gods
]

heroes3map = Sequ(lambda v: maps[v], Uint32, lambda i: p[maps[i]])
