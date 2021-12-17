import sys
import traceback

from PySide2.QtCore import QObject, Signal, QRunnable, Slot


class AsyncSignals(QObject):
    starting = Signal()
    error = Signal(tuple)
    finished = Signal()
    progress = Signal(object)

    def onStarting(self, listener):
        self.starting.connect(listener)

    def onFinished(self, listener):
        self.finished.connect(listener)

    def onError(self, listener):
        self.error.connect(listener)

    def onProgress(self, listener):
        self.progress.connect(listener)


class AsyncFunc(QRunnable):

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = AsyncSignals()

    @Slot()
    def run(self):
        self.signals.starting.emit()
        try:
            self.func(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exception_type, value = sys.exc_info()[:2]
            self.signals.error.emit((exception_type, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()


class Loop:
    def __init__(self, func, mappable):
        self._func = func
        self._mappable = mappable

    def run(self, progress=None):
        for item in self._mappable:
            result = self._func(item)
            if progress:
                progress.emit(result)
