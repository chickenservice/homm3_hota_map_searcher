from PySide2.QtCore import Slot, Signal, QObject

from h3map.filter import AndFilter, MapSizeFilter, TeamSizeFilter, TeamPlayerNumberFilter, Filter


class FilterLibrary(QObject):
    applied = Signal('QVariantMap')
    cleared = Signal()

    def __init__(self, library):
        super().__init__()
        self.library = library

    @Slot('QVariantMap')
    def apply(self, filterForm):
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
        self.applied.emit(summary)

    @Slot()
    def clear(self):
        self.cleared.emit()


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

