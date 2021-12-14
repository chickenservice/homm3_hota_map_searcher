from PySide2.QtCore import Slot, QThreadPool, QObject, Property, Signal

from h3map.gui.asyncFunc import AsyncFunc, Loop
from h3map.header.models import Header
from h3map.library.library import Config


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


class ImportMaps(QObject):
    importMaps = Signal(int)
    importingMaps = Signal(MapSummary)

    importedMap = Signal(MapSummary)

    def __init__(self, library):
        super().__init__()
        self.config = Config()
        self.library = library
        self.threadpool = QThreadPool()

    @Slot(str)
    def importFromFolder(self, directory):
        self.config.set_library_dir(directory)
        files = self.config.detected_map_files()

        self.importMaps.emit(len(files))
        #loop = map(files, self.library.load_map, progress)
        loop = Loop(self.library.load_map, files)
        load_maps = AsyncFunc(loop.run)
        load_maps.signals.onProgress(self._importedMap)

        self.threadpool.start(load_maps)

    def _importedMap(self, mapHeader):
        self.importedMap.emit(MapSummary(mapHeader))
