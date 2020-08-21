from . import observable


def _forwardMethod(key, callHandlersAfter):
    def _(self, *args, **kwargs):
        ret = getattr(self._data, key)(*args, **kwargs)
        if callHandlersAfter:
            self.notify()
        return ret

    return _


class ObservableList(list):
    _observable = True

    def __init__(self, data):
        self._data = [observable(d) for d in data]
        self._handlers = []

    def notify(self):
        for handler in self._handlers:
            handler()

    def _registerItemObserver(self, handler):
        self._handlers.append(handler)

    # Read-only methods
    __str__ = _forwardMethod("__str__", False)
    __repr__ = _forwardMethod("__repr__", False)
    __nonzero__ = _forwardMethod("__nonzero__", False)

    __getitem__ = _forwardMethod("__getitem__", False)
    index = _forwardMethod("index", False)
    count = _forwardMethod("count", False)
    copy = _forwardMethod("copy", False)

    # Writing methods
    pop = _forwardMethod("pop", True)
    clear = _forwardMethod("clear", True)

    def __setitem__(self, index, item):
        self._data[index] = observable(item)
        self.notify()

    def append(self, item):
        self._data.append(observable(item))
        self.notify()

    def extend(self, iterable):
        self._data.extend(observable(d) for d in iterable)
        self.notify()

    def insert(self, index, item):
        self._data.insert(index, observable(item))
        self.notify()