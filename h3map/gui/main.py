import sys
import time
from pathlib import Path

from PySide2.QtCore import Signal, QObject, Slot, Property, QUrl, QSize, QThreadPool
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

from h3map.discover.maps4heroes import DiscoverMaps4Heroes
from h3map.discover.remote_map_loader import FileHtmlMapInfoLoader
from h3map.filter import Filter, MapSizeFilter, TeamSizeFilter, TeamPlayerNumberFilter, AndFilter
from h3map.gui.asyncFunc import Loop, AsyncFunc
from h3map.header.models import Header
from h3map.library.library import Library, Config


class MapSummary(QObject):
    def __init__(self, header: Header, filter_index=None):
        super().__init__()
        self._name = header.metadata.description.name
        self._description = header.metadata.description.summary
        self._teams = header.teams.number_of_teams
        # self._humans = header.humans()
        self._thumbnail = header.metadata.thumbnail
        self._idx = filter_index

    @Property(int)
    def idx(self):
        return self._idx

    @Property(str)
    def name(self):
        return self._name

    @Property(int)
    def teams(self):
        return self._teams

    @Property(int)
    def humans(self):
        return 0
        return self._humans

    @Property(str)
    def description(self):
        return self._description

    @Property(str)
    def thumbnail(self):
        return self._thumbnail


class App(QObject):
    starting = Signal(int)
    progress = Signal(MapSummary)
    addMap = Signal(MapSummary)
    retrievedMaps = Signal(list)
    #filtered = Signal(list)
    filtered = Signal("QVariantMap")
    filterAdded = Signal(int)
    filterCleared = Signal()

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.library = Library()
        self.config = Config()
        self.m4h = DiscoverMaps4Heroes(FileHtmlMapInfoLoader(
            "C:/Users/aless/Projects/Homm3_Hota_Map_Searcher/h3map/reference_maps/maps4heroes.html"))

    @Slot(str)
    def firstTimeImport(self, directory):
        self.config.set_library_dir(directory)
        files = self.config.detected_map_files()

        self.starting.emit(len(files))
        loop = Loop(self.library.load_map, files)
        load_maps = AsyncFunc(loop.run)
        load_maps.signals.onProgress(self.addMap)

        self.threadpool.start(load_maps)

    @Slot(str)
    def load(self, directory):
        self.config.set_library_dir(directory)
        files = self.config.detected_map_files()

        self.starting.emit(len(files))
        loop = Loop(self.library.load_map, files)
        load_maps = AsyncFunc(loop.run)
        load_maps.signals.onProgress(self._addMap)

        self.threadpool.start(load_maps)

    @Slot("QVariantMap")
    def applyFilter(self, filterForm):
        merged = AndFilter()
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

        merged.add(playerFilter.build())
        merged.add(teamSizeFilter.build())
        merged.add(mapSizeFilter.build())

        filtered = self.library.filter_maps(merged)
        summary = {"mapSize": {}, "playerNumber": {}, "teamSize": {}}

        for option in mapSize:
            f = FilterFormAllBuilder()
            f.addFilter(MapSizeFilter, mapSize[option])
            total = AndFilter()
            total.add(f.build())
            total.add(playerFilter.build())
            total.add(teamSizeFilter.build())
            summary["mapSize"][option] = len(self.library.filter_maps(total))

        for option in teamSize:
            f = FilterFormAllBuilder()
            f.addFilter(TeamSizeFilter, teamSize[option])
            total = AndFilter()
            total.add(f.build())
            total.add(playerFilter.build())
            total.add(mapSizeFilter.build())
            summary["teamSize"][option] = len(self.library.filter_maps(total))

        for option in playerNumber:
            f = FilterFormAllBuilder()
            f.addFilter(TeamPlayerNumberFilter, playerNumber[option])
            total = AndFilter()
            total.add(f.build())
            total.add(teamSizeFilter.build())
            total.add(mapSizeFilter.build())
            summary["playerNumber"][option] = len(self.library.filter_maps(total))

        summary["filtered"] = [idx for idx, _ in filtered]
        #self.filtered.emit([MapSummary(header[1], filter_index=header[0]) for header in filtered])
        self.filtered.emit(summary)

    @Slot()
    def filterMaps(self):
        filtered = self.library.filter_maps(self.filter)
        self.filtered.emit([MapSummary(header) for header in filtered])

    @Slot()
    def clearFilter(self):
        #self.filter.clear()
        self.filtered.emit([MapSummary(header, idx) for idx, header in enumerate(self.library.all_maps())])

    @Slot(int)
    def discover(self, requestedAmountOfItems):
        discoverMaps = self.m4h.list_maps(requested=requestedAmountOfItems)
        self.retrievedMaps.emit([MapSummary(header) for header in discoverMaps])

    @Slot(str)
    def download(self, remoteId):
        pass

    def _addMap(self, header):
        self.addMap.emit(MapSummary(header))


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


class QtApp:

    @staticmethod
    def run():
        app = QApplication(sys.argv)

        _app = App()

        view = QQuickView()
        view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
        view.setInitialProperties({"app": _app})
        view.setMinimumSize(QSize(1200, 800))

        qml_file = Path(__file__).parent / "main.qml"
        view.setSource(QUrl.fromLocalFile(str(qml_file)))
        view.show()

        sys.exit(app.exec_())


if __name__ == "__main__":
    QtApp.run()
