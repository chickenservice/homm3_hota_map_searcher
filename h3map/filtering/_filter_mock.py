import sys
from pathlib import Path

from PySide2.QtCore import QSize, QUrl, Slot, Signal, QObject
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication


class FilterMock(QObject):
    applied = Signal('QVariantMap')
    cleared = Signal()

    @Slot('QVariantMap')
    def apply(self, filterForm):
        print('apply')

    @Slot()
    def clear(self):
        print('clear')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    view = QQuickView()
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setInitialProperties({"filterMock": FilterMock()})
    view.setMinimumSize(QSize(1200, 800))

    qml_file = Path(__file__).parent / "FilterBarMock.qml"
    view.setSource(QUrl.fromLocalFile(str(qml_file)))
    view.show()

    sys.exit(app.exec_())
