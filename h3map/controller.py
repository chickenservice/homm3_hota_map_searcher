import glob
import gzip

from h3map.filter import HeaderFilter
from h3map.header.map_reader import MapReader


class MainController:
    def load(self, files):
        maps = {}
        if not len(files):
            files = glob.glob("*.h3m")
        for i, map_file in enumerate(files):
            map_contents = gzip.open(map_file, 'rb').read()
            try:
                header = MapReader.parse(map_contents)
                maps[map_file] = header
            except Exception as e:
                print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)

        return maps

    def filter(self, maps, size=None, teams=None, win=None, loss=None, team_players=None):
        header_filter = HeaderFilter()
        if size is not None:
            header_filter.has_map_size(size)
        if teams is not None:
            header_filter.has_team_size(int(teams))
        if win is not None:
            header_filter.has_win_or_loss_condition(win)
        if loss is not None:
            header_filter.has_win_or_loss_condition(loss)
        if team_players is not None:
            if teams is None:
                raise ValueError("Cannot specify number of players per team without number of teams.")

            header_filter.team_has_players(int(team_players))

        return header_filter.apply(maps.values())
