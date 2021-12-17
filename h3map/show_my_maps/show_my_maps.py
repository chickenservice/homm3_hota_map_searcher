import glob
import gzip
import sys
from pathlib import Path
from typing import Protocol

from PySide2.QtCore import Slot, QThreadPool, QObject, Signal, QSize, QUrl, Property
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

from h3map.asyncFunc import AsyncFunc
from h3map.filtering.filter import Filter, AndFilter, MapSizeFilter, TeamSizeFilter, TeamPlayerNumberFilter
from h3map.header.map_reader import MapReader
from h3map.header.models import Header


def _toDict(header: Header, idx=0):
    header_dict = {}
    header_dict["idx"] = idx
    header_dict["name"] = header.metadata.description.name
    header_dict["description"] = header.metadata.description.summary
    header_dict["humans"] = 0
    header_dict["teams"] = header.teams.number_of_teams
    header_dict["teams"] = header.teams.number_of_teams
    header_dict["thumbnail"] = "default.gif"

    return header_dict


class FilterFormSelectionBuilder:
    def __init__(self):
        self._filters = []

    def addFilter(self, strategy, option):
        if option["selected"]:
            self._filters.append(strategy(option["value"]))

    def build(self):
        f = Filter()
        for i in self._filters:
            f.add_rule(i)
        return f


class FilterFormAllBuilder:
    def __init__(self, filters=None):
        self._filters = filters._filters if filters else []

    def addFilter(self, strategy, option):
        self._filters.append(strategy(option["value"]))

    def build(self):
        f = Filter()
        for i in self._filters:
            f.add_rule(i)
        return f


class ShowMyMapsView(QObject):
    importingMaps = Signal(int)
    importedMap = Signal('QVariantMap')
    configuredChanged = Signal()

    applied = Signal('QVariantMap')
    cleared = Signal()

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.my_maps = None
        self._maps_configured = True

    def show_my_maps(self, my_maps):
        self.my_maps = my_maps

        app = QApplication(sys.argv)

        view = QQuickView()
        view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
        view.setInitialProperties({"importToLibrary": self})
        view.setMinimumSize(QSize(1200, 800))

        qml_file = Path(__file__).parent.parent / "main.qml"
        view.setSource(QUrl.fromLocalFile(str(qml_file)))
        view.show()

        sys.exit(app.exec_())

    def please_set_your_maps_location(self):
        self._maps_configured = False
        self.configuredChanged.emit()

    def show_my_maps_view(self):
        self._maps_configured = True
        self.configuredChanged.emit()

    def show_filtered_maps(self, summary: dict):
        self.applied.emit(summary)

    def show_map_overview(self, header):
        self.importedMap.emit(_toDict(header))

    def show_amount_of_maps_to_import(self, amount: int):
        self.importingMaps.emit(amount)

    @Property(bool, notify=configuredChanged)
    def mapsDirectoryConfigured(self):
        return self._maps_configured

    @Slot(str)
    def importMaps(self, path):
        def _import():
            self.my_maps.import_maps(path)

        self.threadpool.start(AsyncFunc(_import))

    @Slot('QVariantMap')
    def apply(self, filterForm):
        mapSizeFilter = FilterFormSelectionBuilder()
        teamSizeFilter = FilterFormSelectionBuilder()
        playerFilter = FilterFormSelectionBuilder()

        mapSize = filterForm["mapSizeOptions"]
        mapSizeFilter.addFilter(MapSizeFilter, mapSize["XL"])
        mapSizeFilter.addFilter(MapSizeFilter, mapSize["L"])
        mapSizeFilter.addFilter(MapSizeFilter, mapSize["M"])
        mapSizeFilter.addFilter(MapSizeFilter, mapSize["S"])

        teamSize = filterForm["teamSizeOptions"]
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["0"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["1"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["2"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["3"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["4"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["5"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["6"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["7"])
        teamSizeFilter.addFilter(TeamSizeFilter, teamSize["8"])

        playerNumber = filterForm["playerNumberOptions"]
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["0"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["1"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["2"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["3"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["4"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["5"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["6"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["7"])
        playerFilter.addFilter(TeamPlayerNumberFilter, playerNumber["8"])

        self.my_maps.filter_summary(playerFilter.build(), teamSizeFilter.build(), mapSizeFilter.build())

    @Slot()
    def clear(self):
        self.cleared.emit()


class Display(Protocol):
    def show_my_maps(self, my_maps):
        """"""

    def please_set_your_maps_location(self):
        """"""

    def show_map_overview(self, header):
        """"""

    def show_amount_of_maps_to_import(self, amount: int):
        """"""

    def show_my_maps_view(self):
        """"""

    def show_filtered_maps(self, summary: dict):
        """"""

class MyMaps:
    def __init__(self):
        self.maps = []
        self._idx = {}
        self._library_dir = ""

    @property
    def has_location(self):
        return len(self._library_dir)

    def save_my_maps_location(self, directory):
        self._library_dir = directory

    def list(self):
        exp = str(Path(self._library_dir) / "*.h3m")
        return glob.glob(exp[8:])

    def add(self, header: Header):
        self.maps.append(header)
        self._idx[header.metadata.description.name] = len(self.maps) - 1

    def all(self):
        return self.maps

    def filter(self, filter_spec):
        headers = filter_spec.apply(self.all())
        return [(self.index(header), header) for header in headers]

    def index(self, header):
        return self._idx[header.metadata.description.name]


class Map:
    @staticmethod
    def read(path):
        try:
            map_contents = gzip.open(path, 'rb').read()
            return MapReader.parse(map_contents)
        except Exception as e:
            print("Sorry map couldn't be loaded for " + path + " due to an error: ", e)


class ShowMyMaps:
    def __init__(self, display: Display):
        self._maps = MyMaps()
        self._reader = Map
        self._display = display

    def filter_summary(self, number_of_players: Filter = None, team_size: Filter = None, map_size: Filter = None):
        f = AndFilter()
        f.add(number_of_players)
        f.add(team_size)
        f.add(map_size)

        filtered = self._maps.filter(f)
        summary = {"mapSize": {}, "playerNumber": {}, "teamSize": {}}

        for option in MapSizeFilter.sizes():
            total = AndFilter()
            total.add(MapSizeFilter(option))
            total.add(number_of_players)
            total.add(team_size)
            summary["mapSize"][option] = len(self._maps.filter(total))

        for option in range(0, 8):
            total = AndFilter()
            total.add(TeamSizeFilter(option))
            total.add(number_of_players)
            total.add(map_size)
            summary["teamSize"][str(option)] = len(self._maps.filter(total))

        for option in range(0, 8):
            total = AndFilter()
            total.add(TeamPlayerNumberFilter(option))
            total.add(team_size)
            total.add(map_size)
            summary["playerNumber"][str(option)] = len(self._maps.filter(total))

        summary["filtered"] = [idx for idx, _ in filtered]
        self._display.show_filtered_maps(summary)

    def import_maps(self, location: str):
        self._maps.save_my_maps_location(location)
        self._display.show_my_maps_view()
        maps_to_import = self._maps.list()
        self._display.show_amount_of_maps_to_import(len(maps_to_import))
        for map_ in maps_to_import:
            header = self._reader.read(map_)
            self._maps.add(header)
            self._display.show_map_overview(header)

    def show(self):
        if not self._maps.has_location:
            self._display.please_set_your_maps_location()

        self._display.show_my_maps(self)


if __name__ == "__main__":
    view = ShowMyMapsView()
    ShowMyMaps(view).show()
