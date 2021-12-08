import sys
from pathlib import Path

from PySide2.QtCore import Signal, QObject, Slot, Property, QUrl, QSize, QThreadPool
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

from h3map.controller import MainController
from h3map.discover.maps4heroes import DiscoverMaps4Heroes
from h3map.discover.remote_map_loader import FileHtmlMapInfoLoader
from h3map.gui.asyncFunc import Loop, AsyncFunc
from h3map.header.models import Header


class MapSummary(QObject):
    def __init__(self, header: Header):
        super().__init__()
        self._name = header.metadata.description.name
        self._description = header.metadata.description.summary
        self._teams = header.teams.number_of_teams
        # self._humans = header.humans()
        self._thumbnail = header.metadata.thumbnail

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

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.m4h = DiscoverMaps4Heroes(FileHtmlMapInfoLoader(
            "C:/Users/aless/Projects/Homm3_Hota_Map_Searcher/h3map/reference_maps/maps4heroes.html"))

    @Slot(str)
    def load(self, directory):
        controller = MainController()
        files = controller.scan_directory(directory)

        self.starting.emit(len(files))
        loop = Loop(controller.load_map, files)
        load_maps = AsyncFunc(loop.run)
        load_maps.signals.onProgress(self.ntf)

        self.threadpool.start(load_maps)

    @Slot(int)
    def discover(self, requestedAmountOfItems):
        discoverMaps = self.m4h.list_maps(requested=requestedAmountOfItems)
        self.retrievedMaps.emit([MapSummary(header) for header in discoverMaps])

    @Slot(object)
    def ntf(self, header):
        self.progress.emit(MapSummary(header))
        self.addMap.emit(MapSummary(header))


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
