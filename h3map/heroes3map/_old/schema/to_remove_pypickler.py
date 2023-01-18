import logging
import struct

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


class Primitive:
    def __init__(self, fmt):
        self._fmt, self._size = Primitive.__fmts[fmt]

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


Bool = Primitive('bool')
Uchar = Primitive('uint8')
Uint8 = Primitive('uint8')
Uint16 = Primitive('uint16')
Uint32 = Primitive('uint32')


class _String:
    def __init__(self, size):
        self._size = size

    def pickle(self, val, state):
        state.write(struct.pack(f'{self._size}s', bytes(val, encoding='utf-8')))
        return state

    def unpickle(self, state):
        return struct.unpack(f'{self._size}s', state.read(self._size))[0], state


class String:
    def __init__(self):
        self._sequ = Sequ(len, Uint32, _String)

    def pickle(self, val, state):
        s = self._sequ.pickle(val, state)
        return s

    def unpickle(self, state):
        return self._sequ.unpickle(state)


# (b -> a) -> PU a -> (a -> PU b) -> PU b
class Sequ:
    def __init__(self, f, pa, k):
        self._f = f
        self._pa = pa
        self._k = k

    def pickle(self, b, state):
        a = self._f(b)
        pb = self._k(a)
        self._pa.pickle(a, state)
        pb.pickle(b, state)
        return state

    def unpickle(self, state):
        a, s = self._pa.unpickle(state)
        pb = self._k(a)
        return pb.unpickle(state)


# (a -> Int) -> [PU a] -> PU a
class Alt:
    def __init__(self, tag, ps):
        self._tag = tag
        self._ps = ps

    def pickle(self, a, stream):
        n = Uint8 if len(self._ps) == 2 else Uint32  # mimics zeroTo n
        Sequ(self._tag, n, lambda i: self._ps[i]).pickle(a, stream)
        return stream

    def unpickle(self, stream):
        n = Uint8 if len(self._ps) <= 256 else Uint32  # mimics zeroTo n
        return Sequ(self._tag, n, lambda i: self._ps[i]).unpickle(stream)[0], stream


# PU b -> (a -> Int) -> [PU a] -> PU a
class AltP:
    def __init__(self, tag, sel, ps):
        self._tag = tag
        self._ps = ps
        self._sel = sel

    def pickle(self, a, stream):
        n = Uint8 if len(self._ps) <= 256 else Uint32  # mimics zeroTo n
        Sequ(self._tag, n, lambda i: self._ps[self._sel(i)]).pickle(a, stream)
        return stream

    def unpickle(self, stream):
        n = Uint8 if len(self._ps) <= 256 else Uint32  # mimics zeroTo n
        return Sequ(self._tag, n, lambda i: self._ps[self._sel(i)]).unpickle(stream)[0], stream

class IfThen:
    def __init__(self, sel, pa):
        self._alt = AltP(lambda b: 1 if b else 0, sel, [Lift(None), Wrap(self._ident, self._ident, pa)])

    def pickle(self, val, state):
        return self._alt.pickle(val, state)

    def unpickle(self, state):
        return self._alt.unpickle(state)[0], state

    @staticmethod
    def _ident(x): return x


class Maybe:
    def __init__(self, pa):
        self._alt = Alt(lambda b: 1 if b else 0, [Lift(None), Wrap(self._ident, self._ident, pa)])

    def pickle(self, val, state):
        return self._alt.pickle(val, state)

    def unpickle(self, state):
        return self._alt.unpickle(state)[0], state

    @staticmethod
    def _ident(x): return x


class Wrap:
    def __init__(self, i, j, pa):
        self._sequ = Sequ(j, pa, lambda v: Lift(i(v)))

    def pickle(self, val, state):
        return self._sequ.pickle(val, state)

    def unpickle(self, state):
        return self._sequ.unpickle(state)


class KWrap:
    def __init__(self, t, **kwpa):
        self._wrap = Wrap(lambda kw: t(*kw), lambda v: tuple(getattr(v, k) for k in kwpa.keys()), Tuple(list(kwpa.values())))

    def pickle(self, val, state):
        return self._wrap.pickle(val, state)

    def unpickle(self, state):
        val, s = self._wrap.unpickle(state)
        LOGGER.info(val)
        return val, s


# PU a -> Int -> PU [a]
class FixedList:
    def __init__(self, pa, n):
        self._pa = pa
        self._n = n

    def pickle(self, val, state):
        ss = [self._pa.pickle(v, state) for v in val]
        return state

    def unpickle(self, state):
        return [self._pa.unpickle(state)[0] for _ in range(0, self._n)], state


# PU a -> Int -> PU [a]
class List:
    def __init__(self, pa):
        self._pa = pa

    def pickle(self, val, stream):
        length = len(val)
        Uint32.pickle(length, stream)
        FixedList(self._pa, length).pickle(val, stream)
        return stream

    def unpickle(self, stream):
        return FixedList(self._pa, Uint32.unpickle(stream)[0]).unpickle(stream)


# PU a -> Int -> PU [a]
class PList:
    def __init__(self, plen, pa):
        self._pa = pa
        self._plen = plen

    def pickle(self, val, stream):
        length = len(val)
        self._plen.pickle(length, stream)
        FixedList(self._pa, length).pickle(val, stream)
        return stream

    def unpickle(self, stream):
        return FixedList(self._pa, self._plen.unpickle(stream)[0]).unpickle(stream)


class ArgWrap:
    def __init__(self, *args):
        self._ps = args

    def pickle(self, val, state):
        [p.pickle(v, state) for v, p in zip(val, self._ps)]
        return state

    def unpickle(self, state):
        return [p.unpickle(state) for p in self._ps], state

class Tuple:
    def __init__(self, ps):
        self._ps = ps

    def pickle(self, val, state):
        [p.pickle(v, state) for v, p in zip(val, self._ps)]
        return state

    def unpickle(self, state):
        return list(map(lambda p: p.unpickle(state)[0], self._ps)), state


# a -> PU a
class Lift:
    def __init__(self, val):
        self._val = val

    def pickle(self, val, state):
        return state

    def unpickle(self, state):
        return self._val, state
