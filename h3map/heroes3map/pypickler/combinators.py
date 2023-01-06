from h3map.heroes3map.pypickler.picklers import Uint32, _String, Uint8


# a -> PU a
class Lift:
    def __init__(self, val):
        self._val = val

    def pickle(self, val, state):
        return state

    def unpickle(self, state):
        return self._val, state


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


class ArgWrap:
    def __init__(self, *args):
        self._ps = args

    def pickle(self, val, state):
        [p.pickle(v, state) for v, p in zip(val, self._ps)]
        return state

    def unpickle(self, state):
        return [p.unpickle(state)[0] for p in self._ps], state


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


def alt(tag, ps):
    return Sequ(tag, zero_to(len(ps)), lambda i: ps[i])


def altp(tag, sel, ps):
    return Sequ(tag, zero_to(len(ps)), lambda i: ps[sel(i)])


def wrap(i, j, pa):
    return Sequ(j, pa, lambda v: Lift(i(v)))


def kwrap(t, **kwpa):
    return wrap(lambda kw: kw, lambda v: tuple(getattr(v, k) for k in kwpa.keys()), ArgWrap(*kwpa.values()))


def zero_to(n):
    return Uint8 if n <= 256 else Uint32


def if_then(sel, pa):
    return altp(lambda b: 1 if b else 0, sel, [Lift(None), wrap(ident, ident, pa)])


def maybe(pa):
    return alt(lambda b: 1 if b else 0, [Lift(None), wrap(ident, ident, pa)])


def list_p(pa):
    return Sequ(len, Uint32, lambda n: FixedList(pa, n))


def list_pp(pn, pa):
    return Sequ(len, pn, lambda n: FixedList(pa, n))


def string():
    return Sequ(len, Uint32, _String)


def ident(x): return x
