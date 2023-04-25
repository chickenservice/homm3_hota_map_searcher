import glob
import gzip

import sqlite3
from pathlib import Path

from h3map.heroes3map.map_picklers.maps import heroes3map


def read(path):
    with gzip.open(path, 'rb') as map_contents:
        return heroes3map.unpickle(map_contents)[0]


def read_all():
    errs = []
    con = sqlite3.connect(Path.home() / ".h3map/h3map.db")
    con.execute("PRAGMA foreign_keys = ON")
    c = con.cursor()
    c.execute("BEGIN TRANSACTION")
    for i, p in enumerate(glob.glob("C:/Users/aless/Games/HoMM 3 Complete/MapsBackup/*.h3m")):
        # print(p, end="")

        map_contents = gzip.open(p, 'rb')
        try:
            store(c, i, heroes3map.unpickle(map_contents)[0])
            # print("\033[1;32m [OK]\033[0m")
        except gzip.BadGzipFile as gerr:
            try:
                with open(p, 'rb') as mp:
                    store(c, i, heroes3map.unpickle(mp)[0])
                    # print("\033[1;32m [OK]\033[0m")
            except Exception as e:
                errs.append((p, e))
        except Exception as e:
            print(f"{i}, ", e)
            print("\033[1;31m [FAIL]\033[0m")
            errs.append((p, e))
    print()
    print()
    for err in errs:
        print(f"{err[0]}: {err[1]}")

    c.execute("COMMIT")
    con.commit()
    con.close()


pl_cl = [
    'Red',
    'Blue',
    'Tan',
    'Green',
    'Orange',
    'Purple',
    'Teal',
    'Pink'
]


def get_team(teams, p):
    if teams["number_of_teams"] > 0:
        n = teams["teams"][p] + 1
        return n
    else:
        return p + 1


def store(c, i, map_info):
    c.execute(
        "INSERT INTO map(name, description, version, map_size, difficulty, victory_condition, loss_condition) VALUES(?, ?, ?, ?, ?, ?, ?)",
        (
            map_info["metadata"]["name"],
            map_info["metadata"]["description"],
            map_info["version"],
            map_info["metadata"]["size"],
            map_info["metadata"]["difficulty"],
            map_info["winning_condition"]["name"],
            map_info["loss_condition"]["name"]
        )
    )
    c.execute("SELECT count(*) FROM map")
    mapid = c.fetchone()[0]
    pls = [(pl["can_human_play"], pl["can_computer_play"], mapid, pl_cl[j], get_team(map_info["teams"], j))
           for j, pl in enumerate(map_info["player_infos"]) if pl["can_computer_play"] or pl["can_human_play"]]
    for _p in pls:
        c.execute(
            "INSERT INTO player(can_computer_play, can_human_play, map, player_color, team) VALUES(?, ?, ?, ?, ?)", _p)


def _test():
    with sqlite3.connect(Path.home() / ".h3map/h3map.db") as con:
        c = con.cursor()
        with open('h3map_v1_downgrade.sql') as f:
            downgrade = f.read()
            c.executescript(downgrade)
        with open('h3map_v1_upgrade.sql') as f:
            upgrade = f.read()
            c.executescript(upgrade)
        con.commit()

    read_all()
    print("Test finished")


def _show():
    with sqlite3.connect(Path.home() / ".h3map/h3map.db") as con:
        c = con.cursor()
        max_name_len = c.execute("SELECT length(map.name) as name_len FROM map ORDER BY name_len DESC LIMIT 1").fetchone()[0]
        rows = c.execute("SELECT name, version, map_size, difficulty FROM map LIMIT 100").fetchall()

        print("| {: <30} | {: >7} | {: >4} | {: >10} |".format(*["Name", "Version", "Size", "Difficulty"]))
        print("-"*(max_name_len + 34))
        for idx, row in enumerate(rows):
            try:
                name = row[0].decode('utf-8')
                print(f"| {name: <{max_name_len}} | {row[1]: >7} | {row[2]: >4} | {row[3]: >10} |")
            except:
                pass
            #print(f"|{40<:row[0]} | {row[1]: >20} | {row[2]: >20} | {row[3]: >20} |")

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    sub = p.add_subparsers()

    # test
    test_args = sub.add_parser("test")
    test_args.set_defaults(func=_test)

    # show
    show = sub.add_parser("show")
    show.set_defaults(func=_show)

    args = p.parse_args()
    args.func()
