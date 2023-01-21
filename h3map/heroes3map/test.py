import gzip
import glob
import pprint

from h3map.heroes3map.map_picklers.maps import heroes3map

"""
path = "C:/Users/aless/Games/HoMM 3 Complete/MapsBackup/(AB)_Higher_Ground.h3m"

map_contents = gzip.open(path, 'rb')
m = heroes3map.unpickle(map_contents)[0]
pprint.pprint(m)
"""



errs = []
for p in glob.glob("C:/Users/aless/Games/HoMM 3 Complete/MapsBackup/*.h3m"):
    print(p, end="")

    map_contents = gzip.open(p, 'rb')
    try:
        heroes3map.unpickle(map_contents)
        print("\033[1;32m [OK]\033[0m")
    except gzip.BadGzipFile as gerr:
        try:
            with open(p, 'rb') as mp:
                heroes3map.unpickle(mp)
                print("\033[1;32m [OK]\033[0m")
        except Exception as e:
            errs.append((p, e))
    except Exception as e:
        print(e)
        print("\033[1;31m [FAIL]\033[0m")
        errs.append((p, e))
print()
print()
for err in errs:
    print(f"{err[0]}: {err[1]}")

