import math
import sqlite3
import sys
import typing
from pathlib import Path

from PySide2 import QtCore
from PySide2.QtCore import QSize, QUrl, Slot, Signal, QObject, QThreadPool, QAbstractTableModel, QAbstractListModel, Qt, \
    QModelIndex
from PySide2.QtQuick import QQuickView
from PySide2.QtSql import QSql, QSqlQueryModel, QSqlDatabase
from PySide2.QtWidgets import QApplication

from h3map.asyncFunc import AsyncFunc
from h3map.filtering._filter_mock import Filter, dsizes, sizes


def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'Info'
    elif mode == QtCore.QtWarningMsg:
        mode = 'Warning'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'critical'
    elif mode == QtCore.QtFatalMsg:
        mode = 'fatal'
    else:
        mode = 'Debug'
        print("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file))


def all_maps():
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    con = sqlite3.connect(Path.home() / ".h3map/h3map.db")
    con.row_factory = dict_factory
    c = con.cursor()
    c.execute("SELECT name, description, map_size, difficulty, victory_condition, loss_condition FROM map")
    ms = c.fetchall()
    c.close()
    con.close()
    return ms



def filter_maps_count(ts, pl, ms):
    query = """
    select count(*)
    from map
    where map.id in (select map.id
                     from map
                              left join player p on map.id = p.map
                              join team t on t.id = p.team
                    where map.map_size in ({0})
                     group by map.id
                     having count(p.id) in ({1})
                        and (select count(distinct p.team)) in ({2}));
                    """
    con = sqlite3.connect(Path.home() / ".h3map/h3map.db")
    c = con.cursor()
    c.execute(query.format(', '.join(['?'] * len(ms)), ', '.join(['?'] * len(pl)), ', '.join(['?'] * len(ts))),
              ms + pl + ts)
    ms = c.fetchone()
    con.close()
    return ms[0]


def filter_maps(ts, pl, ms, amount, last=0):
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}
    query = """
    select id, name, description, map_size, difficulty, victory_condition, loss_condition
    from 
     (select row_number() over () as r,  map.id, name, description, map_size, difficulty, victory_condition, loss_condition
                     from map
                              left join player p on map.id = p.map
                              join team t on t.id = p.team
                    where map.map_size in ({0})
                     group by map.id
                     
                     having count(p.id) in ({1})
                        and (select count(distinct p.team)) in ({2}))
        where r >= (?)
        limit (?);
                    """
    con = sqlite3.connect(Path.home() / ".h3map/h3map.db")
    con.row_factory = dict_factory
    c = con.cursor()
    c.execute(query.format(', '.join(['?'] * len(ms)), ', '.join(['?'] * len(pl)), ', '.join(['?'] * len(ts))),
              ms + pl + ts + [last, amount])
    ms = c.fetchall()
    con.close()
    return ms


def page_maps(size, last=0):
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    con = sqlite3.connect(Path.home() / ".h3map/h3map.db")
    con.row_factory = dict_factory
    c = con.cursor()
    c.execute("SELECT map.id, name, description, map_size, difficulty, victory_condition, loss_condition FROM map WHERE map.id >= (?) LIMIT (?)", [last, size])
    ms = c.fetchall()
    c.close()
    con.close()
    return ms


def c():
    con = sqlite3.connect(Path.home() / ".h3map/h3map.db")
    c = con.cursor()
    c.execute("SELECT COUNT(map.id) FROM map")
    ms = c.fetchone()
    c.close()
    con.close()
    return ms[0]


class GenericModel(QtCore.QAbstractListModel):
    roles = {
        Qt.UserRole + 0: 'name',
        Qt.UserRole + 1: 'description',
        Qt.UserRole + 2: 'map_size',
        Qt.UserRole + 3: 'difficulty',
        Qt.UserRole + 4: 'victory_condition',
        Qt.UserRole + 5: 'loss_condition',
        Qt.UserRole + 6: 'id',
    }

    applied = Signal(int, list)

    def __init__(self):
        super().__init__()
        self.ms = page_maps(100, 0)
        self.count = c()
        self.page = 0
        self.fetch = page_maps
        self.threadpool = QThreadPool()
        self.applied.connect(self.onApplied)

    @Slot('QVariantMap')
    def applyFilter(self, form):
        def _params(opts, alt):
            selected = [opts[option]["value"] for option in opts if opts[option]["selected"]]
            if not len(selected):
                return alt
            return selected
        ts = _params(form["teamSizeOptions"], [1, 2, 3, 4, 5, 6, 7, 8])
        pl = _params(form["playerNumberOptions"], [1, 2, 3, 4, 5, 6, 7, 8])
        ms = [dsizes[size] for size in _params(form["mapSizeOptions"], sizes)]

        if len(ts + pl + ms):
            def _f():
                m = filter_maps(ts, pl, ms, 100, 0)
                self.fetch = lambda cs, s: filter_maps(ts, pl, ms, cs, s)
                self.applied.emit(filter_maps_count(ts, pl, ms), m)
            self.threadpool.start(AsyncFunc(_f))
        else:
            def nofilter():
                m = page_maps(100, 0)
                self.fetch = page_maps
                self.applied.emit(c(), m)
            self.threadpool.start(AsyncFunc(nofilter))


    @Slot(int, list)
    def onApplied(self, count, maps):
        self.beginResetModel()
        self.page = 0
        self.ms = maps
        self.count = count
        self.endResetModel()

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return self.count

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self._d[0])

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        idx = index.row()
        p = (idx // 100)
        if p != self.page:
            self.ms = self.fetch(100, p * 100)
            self.page = p

        return self.ms[idx - self.page*100][GenericModel.roles[role]]

    def roleNames(self) -> typing.Dict:
        return {
            Qt.UserRole + 0: b'name',
            Qt.UserRole + 1: b'description',
            Qt.UserRole + 2: b'map_size',
            Qt.UserRole + 3: b'difficulty',
            Qt.UserRole + 4: b'victory_condition',
            Qt.UserRole + 5: b'loss_condition',
            Qt.UserRole + 6: b'id',
        }


class List(QObject):
    itemAdded = Signal('QVariantMap')

    def __init__(self, f):
        super().__init__()
        self.threadpool = QThreadPool()
        self.f = f

    @Slot()
    def items(self):
        self.threadpool.start(AsyncFunc(self._list))

    def _list(self):
        for item in self.f():
            self.itemAdded.emit(item)


if __name__ == "__main__":
    QtCore.qInstallMessageHandler(qt_message_handler)
    app = QApplication(sys.argv)
    l = List(all_maps)
    ll = GenericModel()

    f = Filter
    view = QQuickView()
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setInitialProperties({"libraryModel": l, "pyFilter": f, "table": ll})
    view.setMinimumSize(QSize(1200, 800))

    qml_file = Path(__file__).parent / "MapsV.qml"
    view.setSource(QUrl.fromLocalFile(str(qml_file)))
    view.show()

    sys.exit(app.exec_())
