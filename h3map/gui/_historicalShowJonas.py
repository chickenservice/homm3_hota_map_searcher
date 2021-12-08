import glob
from pathlib import Path

import PySide2
from PySide2.QtCore import QObject, Signal, QAbstractListModel, QModelIndex, QThread, Slot
from qasync import QtCore

from h3map.controller import MainController
from h3map.gui.main import MapSummary
from h3map.header.models import Header


class Worker(QObject):
    starting = Signal(int)
    finished = Signal()
    progress = Signal(Header)

    def __init__(self, observer, dir):
        super().__init__()
        self.obs = observer
        self.dir = dir

    def run(self):
        controller = MainController()
        exp = str(Path(self.dir) / "*.h3m")
        files = glob.glob(exp[8:])
        self.starting.emit(len(files))
        for file in files:
            header = controller.load_map(file)
            self.progress.emit(header)
        self.finished.emit()


class Maps(QAbstractListModel):
    progress = Signal(int)
    col1 = QtCore.Qt.UserRole + 1

    def __init__(self, maps):
        super(Maps, self).__init__()
        self._maps = []
        self._new_maps = []
        for map in maps:
            summary = MapSummary(map)
            self._maps.append(summary)

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self._maps)

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        return self._maps[index.row()]

    def roleNames(self):
        return {Maps.col1: b"data"}

    def load(self):
        self.beginInsertRows(QModelIndex(), len(self._maps), len(self._maps) - 1 + len(self._maps))
        for hmap in self._maps:
            summary = MapSummary(hmap)
            self._maps.append(summary)
        self.endInsertRows()

    def ntf(self, max_count, header):
        self.beginInsertRows(QModelIndex(), len(self._maps), len(self._maps) + 1)
        self._maps.append(MapSummary(header))
        self.endInsertRows()
        self.progress.emit(max_count)

    @Slot(str)
    def loaded(self, dir):
        self.thread = QThread()
        self.worker = Worker(self, dir)
        self.thread.started.connect(self.worker.run)
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.ntf)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

    async def _loaded(self, dir):
        controller = MainController()
        exp = str(Path(dir) / "*.h3m")
        files = glob.glob(exp[8:])
        maps = controller.load(files, observer=self).all()


