import struct

class Pickler:
    def __init__(self, fmt):
        self._fmt, self._size = Pickler.__fmts[fmt]

    def pickle(self, val, state):
        state.write(struct.pack(self._fmt, val))
        return state

    def unpickle(self, state):
        val = struct.unpack(self._fmt, state.read(self._size))[0]
        return val, state

    __fmts = {
        'uint8': ('B', 1),
        'uint16': ('H', 2),
        'uint32': ('i', 4),
        'bool': ('?', 1),
    }


Bool = Pickler('bool')
Uchar = Pickler('uint8')
Uint8 = Pickler('uint8')
Uint16 = Pickler('uint16')
Uint32 = Pickler('uint32')


class _String:
    def __init__(self, size):
        self._size = size

    def pickle(self, val, state):
        state.write(struct.pack(f'{self._size}s', bytes(val, encoding='utf-8')))
        return state

    def unpickle(self, state):
        return struct.unpack(f'{self._size}s', state.read(self._size))[0], state


