import glob
import gzip
import json
import os.path
import sys
from pathlib import Path
from typing import Protocol, List, Union

from PySide2.QtCore import Slot, QThreadPool, QObject, Signal, QSize, QUrl, Property
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication
from sqlalchemy import or_, func, and_, distinct
from sqlalchemy.orm import sessionmaker

from h3map.asyncFunc import AsyncFunc
from h3map.filtering.filter import Filter, AndFilter, MapSizeFilter, TeamSizeFilter, TeamPlayerNumberFilter
from h3map.header.map_reader import MapReader
from h3map.header.models import Header, Metadata, TeamSetup, Description, StandardWinningCondition, \
    StandardLossCondition, MapProperties
from h3map.heroes3 import Player, engine, PlayerColor, Town, Map, MapSize, Version, Difficulty, WinningCondition, \
    LossCondition, Team, Config


def _toDict(header: Header, idx=0):
    header_dict = {}
    header_dict["idx"] = idx
    header_dict["name"] = header.metadata.description.name
    header_dict["description"] = header.metadata.description.summary
    header_dict["humans"] = 0
    header_dict["teams"] = header.teams.number_of_teams
    header_dict["thumbnail"] = "default.gif"

    return header_dict


def _to_header(d: dict):
    description = Description(d["name"], d["description"])
    metadata = Metadata(0, None, description, None)
    metadata.description.name = d["name"]
    metadata.description.summary = d["description"]

    teams = TeamSetup(d["teams"], None)
    teams.number_of_teams = d["teams"]

    return Header(metadata, None, teams, None, None)


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
    importedMaps = Signal()
    configuredChanged = Signal()

    applying = Signal()
    applied = Signal('QVariantMap')
    cleared = Signal()

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.my_maps = None
        self._maps_configured = True

    @Slot()
    def maps(self):
        if self.my_maps and self.mapsDirectoryConfigured:
            def _async():
                # self.my_maps.import_new_maps()
                self.my_maps.load()

            self.threadpool.start(AsyncFunc(_async))

    def show_my_maps(self, my_maps):
        self.my_maps = my_maps

        app = QApplication(sys.argv)

        view = QQuickView()
        view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
        view.setInitialProperties({"importToLibrary": self})
        view.setMinimumSize(QSize(1200, 800))

        qml_file = Path(__file__).parent.parent / "main.qml"
        view.setSource(QUrl('qrc:/main.qml'))
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
        self.importedMap.emit(header)

    def show_amount_of_maps_to_import(self, amount: int):
        self.importingMaps.emit(amount)

    def successful_import(self):
        self.importedMaps.emit()

    @Property(bool, notify=configuredChanged)
    def mapsDirectoryConfigured(self):
        return self._maps_configured

    @Slot(str)
    def importMaps(self, path):
        def _import():
            self.my_maps.import_maps(path[8:])

        self.threadpool.start(AsyncFunc(_import))

    @Slot('QVariantMap')
    def apply(self, filterForm):
        self.applying.emit()
        def _func():
            mapSize = filterForm["mapSizeOptions"]
            sizes = []
            for option in mapSize:
                if mapSize[option]["selected"]:
                    sizes.append(mapSize[option]["value"])

            teamSize = filterForm["teamSizeOptions"]
            teamSizes = []
            for option in teamSize:
                if teamSize[option]["selected"]:
                    teamSizes.append(teamSize[option]["value"])

            playerNumber = filterForm["playerNumberOptions"]
            playerNumbers = []
            for option in playerNumber:
                if playerNumber[option]["selected"]:
                    playerNumbers.append(playerNumber[option]["value"])

            self.my_maps.filter_summary(playerNumbers, teamSizes, sizes)

        self.threadpool.start(AsyncFunc(_func))

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

    def successful_import(self):
        pass


class MyMapsLocation(Protocol):
    @property
    def has_location(self) -> bool:
        """Has user set his maps location?"""

    @property
    def location(self) -> str:
        """Location of the users maps"""

    def save_my_maps_location(self, directory: str):
        """Save the users' original maps location. For now he can only have exactly one location."""


class ReadStore(Protocol):
    def names(self) -> List[str]:
        """"""

    def count(self) -> int:
        """Amount of maps in store"""

    def has(self, path) -> bool:
        """"""

    def all(self) -> List[Header]:
        """Gives a list of the users maps"""


class WriteStore(Protocol):
    def add(self, header: Header):
        """Store a users map"""


class MyMapsFilter(Protocol):
    def filter(self, filter_spec: Filter) -> List[Header]:
        """Get maps based on given filter"""


class MyMapsInDirectory:
    def __init__(self):
        self._library_dir = ""

    @property
    def has_location(self):
        return len(self._library_dir)

    @property
    def location(self) -> str:
        return self._library_dir

    def names(self):
        path = Path(self._library_dir) / "*.h3m"
        return [name for name in os.path.splitext(os.path.basename(path))[0]]

    def has(self, name):
        return True

    def save_my_maps_location(self, directory):
        self._library_dir = directory

    def count(self):
        path = Path(self._library_dir) / "*.h3m"
        return len(glob.glob(str(path)))

    def all(self) -> List[Header]:
        path = Path(self._library_dir) / "*.h3m"
        maps_in_directory = glob.glob(str(path))
        for map_ in maps_in_directory:
            yield self._read(map_)

    @staticmethod
    def _read(path):
        try:
            map_contents = gzip.open(path, 'rb').read()
            header: Header = MapReader.parse(map_contents)
            header.file_path = path
            return header
        except Exception as e:
            print("Sorry map couldn't be loaded for " + path + " due to an error: ", e)
            return None


class MyMapsInMemory:
    def __init__(self):
        self.maps = []
        self._idx = {}

    def add(self, header: Header):
        self.maps.append(header)
        self._idx[header.metadata.description.name] = len(self.maps) - 1

    def count(self):
        return len(self.maps)

    def all(self):
        return self.maps

    def filter(self, filter_spec):
        headers = filter_spec.apply(self.all())
        return [(self.index(header), header) for header in headers]

    def index(self, header):
        return self._idx[header.metadata.description.name]


class MyMapsJson:
    def __init__(self):
        self._storage_path = "C:/Users/aless/Projects/Homm3_Hota_Map_Searcher/.cache"

    @property
    def has_location(self) -> bool:
        return True if len(self.location) else False

    @property
    def location(self):
        path: Path = self._path()
        if not path.exists():
            return ""

        with open(path, 'r') as fp:
            config = json.load(fp)

        return config["my maps"]

    def save_my_maps_location(self, directory: str):
        path: Path = self._path()
        with open(path, 'w') as fp:
            json.dump({"my maps": directory, "headers": {}}, fp)

    def names(self):
        headers = self.all()
        return [os.path.splitext(name.file_path)[0] for name in headers]

    def has(self, name):
        return name in self.names()

    def add(self, header: Header):
        header_as_dict = _toDict(header)
        with open(self._path(), 'r') as fp:
            h3m = json.load(fp)
        with open(self._path(), 'w') as fp:
            h3m["headers"][header_as_dict["name"]] = header_as_dict
            json.dump(h3m, fp)

    def count(self):
        path = Path(self._storage_path) / "*.json"
        return len(glob.glob(path))

    def all(self):
        headers = []
        with open(self._path()) as fp:
            h3m = json.load(fp)
            for header in h3m["headers"].values():
                headers.append(_to_header(header))

        return headers

    def _path(self):
        return Path(self._storage_path) / "h3map.json"


class MyMapsSqlite:
    def __init__(self):
        self._sqlite_db_path = "C:/Users/aless/Projects/Homm3_Hota_Map_Searcher/.cache/h3map.db"
        self._session = sessionmaker(bind=engine)

    @property
    def has_location(self) -> bool:
        with self._session() as session, session.begin():
            return session.query(Config).count() > 0

    @property
    def location(self) -> str:
        with self._session() as session, session.begin():
            return session.query(Config.maps_location).first()

    def save_my_maps_location(self, directory: str):
        with self._session() as session, session.begin():
            session.add(Config(maps_location=directory))

    def add(self, header: Header):
        players = []
        with self._session() as session, session.begin():
            for player in header.players_info:
                color = session.query(PlayerColor).where(PlayerColor.id == player.id + 1).first()
                team = session.query(Team).where(
                    Team.id == header.teams.teams[player.id] + 1).first()
                towns = session.query(Town).filter(Town.name.in_(player.faction_info.factions)).all()
                p = Player(player_color=color, team=team, towns=towns, can_computer_play=player.who_can_play.can_computer_play, can_human_play=player.who_can_play.can_human_play)
                players.append(p)

            loss_cond = session.query(LossCondition).where(LossCondition.id == header.loss_condition + 1).first()
            win_cond = session.query(WinningCondition).where(WinningCondition.id == header.winning_condition + 1).first()

            map_ = Map(name=header.metadata.description.name,
                       description=header.metadata.description.summary,
                       any_players=header.metadata.properties.any_players,
                       version=session.query(Version).where(Version.version == header.metadata.version.version).first(),
                       difficulty=session.query(Difficulty).where(
                           Difficulty.difficulty == header.metadata.difficulty.difficulty).first(),
                       map_size=session.query(MapSize).where(MapSize.size == header.metadata.properties.size).first(),
                       players=players,
                       winning_condition=win_cond,
                       loss_condition=loss_cond,
                       )
            session.add(map_)

    def all(self):
        with self._session() as session, session.begin():
            maps = session.query(Map).all()
            ms = []
            for m in maps:
                teams = session.query(Player.id, Player.team_id) \
                    .filter(Player.map_id == m.id) \
                    .distinct(Player.team_id) \
                    .group_by(Player.team_id) \
                    .count()
                humans = session.query(Player.id)\
                    .filter(Player.map_id == m.id)\
                    .filter(Player.can_human_play)\
                    .count()
                ms.append(self._to_dict(m, teams=teams, humans=humans))
            return ms

    def _to_dict(self, m: Map, teams=0, humans=0):
        header_dict = {}
        header_dict["idx"] = m.id
        header_dict["name"] = m.name
        header_dict["description"] = m.description
        header_dict["players"] = len(m.players) if m.players else 0
        header_dict["humans"] = humans
        header_dict["teams"] = teams
        header_dict["size"] = m.map_size.name
        header_dict["difficulty"] = m.difficulty.name
        header_dict["thumbnail"] = "default.gif"
        header_dict["win_cond"] = m.winning_condition.name if m.winning_condition else ""
        header_dict["loss_cond"] = m.loss_condition.name if m.loss_condition else ""

        return header_dict


class ShowMyMaps:
    def __init__(self, display: Display):
        self._maps = MyMapsInDirectory()
        self._store = MyMapsJson()
        self._cache = MyMapsInMemory()
        self._display = display

    def _filter(self, vals, entity):
        _vals = []
        for val in vals:
            _vals.append(func.count(entity) == val)

        return _vals

    def _filter2(self, vals, entity):
        _vals = []
        for val in vals:
            _vals.append(func.count(distinct(entity)) == val)

        return _vals

    def filter_summary(self, number_of_players=None, team_size=None, map_size=None):
        map_filter: MyMapsFilter = self._cache

        f = AndFilter()
        f.add(number_of_players)
        f.add(team_size)
        f.add(map_size)
        _session = sessionmaker(bind=engine)
        with _session() as session, session.begin():
            nums = self._filter(number_of_players, Player.id)
            nums_team = self._filter2(team_size, Player.team_id)
            sizes = [Map.map_size == session.query(MapSize).filter(MapSize.name == s).first() for s in map_size]
            maps = session.query(Map.id)\
                .filter(and_(or_(*sizes)))\
                .outerjoin(Map.players) \
                .join(Player.team)\
                .group_by(Map.id) \
                .having(and_(or_(*nums), or_(*nums_team)))\
                .all()

            summary = {"mapSize": {}, "playerNumber": {}, "teamSize": {}}
            summary["filtered"] = [m.id - 1 for m in maps]

            for option in MapSizeFilter.sizes():
                s = session.query(MapSize).where(MapSize.name == option).first()
                c = session.query(Map.id) \
                    .filter(Map.map_size == s) \
                    .outerjoin(Map.players) \
                    .join(Player.team) \
                    .group_by(Map.id) \
                    .having(and_(or_(*nums), or_(*nums_team))) \
                    .count()

                summary["mapSize"][option] = c

            for option in range(2, 9):
                c = session.query(Map.id) \
                    .filter(and_(or_(*sizes))) \
                    .outerjoin(Map.players) \
                    .join(Player.team) \
                    .group_by(Map.id) \
                    .having(and_(or_(*nums), func.count(distinct(Player.team_id)) == option)) \
                    .count()
                summary["teamSize"][str(option)] = c
                
            for option in range(1, 9):
                p = func.count(Player.id) == option
                c = session.query(Map.id) \
                    .filter(and_(or_(*sizes))) \
                    .outerjoin(Map.players) \
                    .join(Player.team) \
                    .group_by(Map.id) \
                    .having(and_(p, or_(*nums_team))) \
                    .count()

                summary["playerNumber"][str(option)] = c
                
        self._display.show_filtered_maps(summary)

    def import_maps(self, location: str):
        my_location: Union[MyMapsLocation, ReadStore] = self._maps
        display: Display = self._display
        store: Union[WriteStore, MyMapsLocation] = MyMapsSqlite()
        cache: WriteStore = self._cache

        my_location.save_my_maps_location(location)
        store.save_my_maps_location(location)
        display.show_my_maps_view()
        display.show_amount_of_maps_to_import(my_location.count())
        for map_ in self._maps.all():
            if map_ is None:
                continue
            store.add(map_)
            cache.add(map_)
            display.show_map_overview(_toDict(map_))

        display.successful_import()

    def import_new_maps(self):
        """TODO: unfinished check for new maps"""
        my_location: Union[MyMapsLocation, ReadStore] = self._maps
        display: Display = self._display
        store: Union[WriteStore, ReadStore, MyMapsLocation] = self._store
        cache: WriteStore = self._cache

        my_location.save_my_maps_location(store.location)

        new = [new_ for new_ in my_location.all() if store.has(new_)]
        display.show_amount_of_maps_to_import(len(new))
        for map_ in my_location.all():
            store.add(map_)
            cache.add(map_)
            display.show_map_overview(map_)

        display.successful_import()

    def load(self):
        display: Display = self._display
        store: Union[ReadStore, MyMapsLocation] = MyMapsSqlite()

        display.show_my_maps_view()
        for map_ in store.all():
            display.show_map_overview(map_)

        display.successful_import()

    def maps(self):
        return self._cache.maps

    def show(self):
        store: MyMapsLocation = MyMapsSqlite()
        display: Display = self._display

        if not store.has_location:
            display.please_set_your_maps_location()

        display.show_my_maps(self)

    def _scan_new_maps(self):
        directory: MyMapsLocation = self._maps
        store: MyMapsLocation = self._store

        return [new for new in directory.listing() if not store.has(new)]


if __name__ == "__main__":
    view = ShowMyMapsView()
    ShowMyMaps(view).show()
