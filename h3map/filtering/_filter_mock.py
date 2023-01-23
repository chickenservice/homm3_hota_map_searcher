import sqlite3
import sys
from pathlib import Path

from PySide2.QtCore import QSize, QUrl, Slot, Signal, QObject, QThreadPool
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

from h3map.asyncFunc import AsyncFunc


sizes = ["S", "M", "L", "XL", "H", "XH", "G"]
dsizes = {"S": 36, "M": 72, "L": 108, "XL":144, "H":180, "XH":216, "G":252}
ddsizes = {36: "S", 72: "M", 108: "L", 144: "XL", 180: "H", 216: "XH", 252: "G"}

class Filter(QObject):
    applied = Signal('QVariantMap')
    cleared = Signal()

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()

    @Slot('QVariantMap')
    def apply(self, filterForm):
        def _func():
            con = sqlite3.connect(Path.home() / ".h3map/h3map.db")
            c = con.cursor()

            summary = {"mapSize": {}, "playerNumber": {}, "teamSize": {}}

            ts = self._count(filterForm["teamSizeOptions"], [1, 2, 3, 4, 5, 6, 7, 8])
            pl = self._count(filterForm["playerNumberOptions"], [1, 2, 3, 4, 5, 6, 7, 8])
            ms = [dsizes[size] for size in self._count(filterForm["mapSizeOptions"], sizes)]
            summary["mapSize"] = self._maps(c, ts, pl)
            summary["playerNumber"] = self._players(c, ms, ts)
            summary["teamSize"] = self._teams(c, ms, pl)

            self.applied.emit(summary)
            con.close()

        self.threadpool.start(AsyncFunc(_func))

    def _count(self, opts, alt):
        selected = [opts[option]["value"] for option in opts if opts[option]["selected"]]
        if not len(selected):
            return alt
        return selected

    def _teams(self, c, m, p):
        query = """
select teamsize, count(*)
from (select count(distinct p.team) as teamsize
      from map
               left join player p on map.id = p.map
               join team t on t.id = p.team
      where map.map_size in ({0})
      group by map.id
      having count(p.id) in ({1}))
group by teamsize;
                """
        c.execute(query.format(', '.join(['?'] * len(m)), ', '.join(['?'] * len(p))), m+p)
        res = c.fetchall()
        result = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}
        for i, r in enumerate(res):
            result[str(r[0] - 1)] = r[1]
        return result

    def _players(self, c, m, t):
        query = """
select c, count(*)
from (select count(*) as c
      from map
               left join player p on map.id = p.map
               join team t on t.id = p.team
      where map.map_size in ({0})
      group by map.id
      having count(p.id) in (1, 2, 3, 4, 5, 6, 7, 8)
         and (select count(distinct p.team)) in ({1}))
group by c;
                """
        c.execute(query.format(', '.join(['?'] * len(m)), ', '.join(['?'] * len(t))), m + t)
        res = c.fetchall()
        result = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}
        for i, r in enumerate(res):
            result[str(r[0] - 1)] = r[1]
        return result


    def _maps(self, c, selT, selP):
        query = """
select map.map_size, count(*)
from map
where map.id in (select map.id
                 from map
                          left join player p on map.id = p.map
                          join team t on t.id = p.team
                 group by map.id
                 having count(p.id) in ({0})
                    and (select count(distinct p.team)) in ({1}))
group by map.map_size;
                """
        c.execute(query.format(', '.join(['?'] * len(selP)), ', '.join(['?'] * len(selT))), selP+selT)
        res = c.fetchall()
        result = {"S": 0, "M": 0, "L": 0, "XL": 0, "H": 0, "XH": 0, "G": 0}
        for i, r in enumerate(res):
            result[ddsizes[r[0]]] = r[1]
        return result

    @Slot()
    def clear(self):
        print('clear')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Filter()

    view = QQuickView()
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setInitialProperties({"filterMock": f})
    view.setMinimumSize(QSize(1200, 800))

    qml_file = Path(__file__).parent / "FilterBarMock.qml"
    view.setSource(QUrl.fromLocalFile(str(qml_file)))
    view.show()

    sys.exit(app.exec_())
