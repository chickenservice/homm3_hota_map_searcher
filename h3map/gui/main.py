import sys
import time
from pathlib import Path

from PySide2.QtCore import Signal, QObject, Slot, Property, QUrl, QSize, QThreadPool
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

from h3map.discover.maps4heroes import DiscoverMaps4Heroes
from h3map.discover.remote_map_loader import FileHtmlMapInfoLoader
from h3map.filter import Filter, MapSizeFilter, TeamSizeFilter, TeamPlayerNumberFilter
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
    filtered = Signal(list)
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
        #if "mapSizeOptions" in filterForm:
        #   options = filterForm["mapSizeOptions"]
        #   for option in options:
        #       builder.addFilter(MapSizeFilter, option[options])
        builder = FilterFormBuilder()

        mapSize = filterForm["mapSizeOptions"]
        builder.addFilter(MapSizeFilter, mapSize["XL"])
        builder.addFilter(MapSizeFilter, mapSize["L"])
        builder.addFilter(MapSizeFilter, mapSize["M"])
        builder.addFilter(MapSizeFilter, mapSize["S"])

        teamSize = filterForm["teamSizeOptions"]
        builder.addFilter(TeamSizeFilter, teamSize["0"])
        builder.addFilter(TeamSizeFilter, teamSize["1"])
        builder.addFilter(TeamSizeFilter, teamSize["2"])
        builder.addFilter(TeamSizeFilter, teamSize["3"])
        builder.addFilter(TeamSizeFilter, teamSize["4"])
        builder.addFilter(TeamSizeFilter, teamSize["5"])
        builder.addFilter(TeamSizeFilter, teamSize["6"])
        builder.addFilter(TeamSizeFilter, teamSize["7"])
        builder.addFilter(TeamSizeFilter, teamSize["8"])

        playerNumber = filterForm["playerNumberOptions"]
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["0"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["1"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["2"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["3"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["4"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["5"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["6"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["7"])
        builder.addFilter(TeamPlayerNumberFilter, playerNumber["8"])

        start = time.time()
        filtered = self.library.filter_maps(builder.build())
        self.filtered.emit([MapSummary(header[1], filter_index=header[0]) for header in filtered])

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


class FilterFormBuilder:
    def __init__(self):
        self._filter = Filter()

    def addFilter(self, strategy, option):
        if option["selected"]:
            self._filter.add_rule(strategy(option["value"]))

    def build(self):
        return self._filter


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
