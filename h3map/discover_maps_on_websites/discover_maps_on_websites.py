from PySide2.QtCore import QObject, Signal, Slot

from h3map.discover_maps_on_websites.maps4heroes import DiscoverMaps4Heroes
from h3map.discover_maps_on_websites.remote_map_loader import FileHtmlMapInfoLoader


class App(QObject):
    retrievedMaps = Signal(list)

    def __init__(self):
        super().__init__()
        self.m4h = DiscoverMaps4Heroes(FileHtmlMapInfoLoader(
            "/h3map/_reference_maps/maps4heroes.html"))

    @Slot(int)
    def discover(self, requestedAmountOfItems):
        discoverMaps = self.m4h.list_maps(requested=requestedAmountOfItems)
        self.retrievedMaps.emit([header for header in discoverMaps])

    @Slot(str)
    def download(self, remoteId):
        pass


