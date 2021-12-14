import sys
from pathlib import Path

from PySide2.QtCore import Signal, QObject, Slot, QUrl, QSize
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

from h3map.discover.maps4heroes import DiscoverMaps4Heroes
from h3map.discover.remote_map_loader import FileHtmlMapInfoLoader
from h3map.gui.ImportMaps import ImportMaps, MapSummary
from h3map.gui.library import FilterLibrary
from h3map.library.library import Library


class App(QObject):
    retrievedMaps = Signal(list)

    def __init__(self):
        super().__init__()
        self.m4h = DiscoverMaps4Heroes(FileHtmlMapInfoLoader(
            "C:/Users/aless/Projects/Homm3_Hota_Map_Searcher/h3map/reference_maps/maps4heroes.html"))

    @Slot(int)
    def discover(self, requestedAmountOfItems):
        discoverMaps = self.m4h.list_maps(requested=requestedAmountOfItems)
        self.retrievedMaps.emit([MapSummary(header) for header in discoverMaps])

    @Slot(str)
    def download(self, remoteId):
        pass


class QtApp:

    @staticmethod
    def run():
        app = QApplication(sys.argv)

        _app = App()

        library = Library()
        filterLibrary = FilterLibrary(library)
        importMaps = ImportMaps(library)

        view = QQuickView()
        view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
        view.setInitialProperties({"app": _app,  "importToLibrary": importMaps, "filterLibrary": filterLibrary})
        view.setMinimumSize(QSize(1200, 800))

        qml_file = Path(__file__).parent / "main.qml"
        view.setSource(QUrl.fromLocalFile(str(qml_file)))
        view.show()

        sys.exit(app.exec_())


if __name__ == "__main__":
    QtApp.run()
