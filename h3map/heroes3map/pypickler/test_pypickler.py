import logging
from dataclasses import dataclass
import io

from picklers import Uint8
from combinators import List, FixedList, Wrap, Tuple, Uint8, String, Maybe, KWrap, ArgWrap

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def test_list():
    l = [0, 1, 2, 3, 4, 5]
    b = len(l).to_bytes() + bytes(l)

    stream = io.BytesIO(b)

    p = FixedList(Uint8, Uint8(stream))
    return p.unpickle(stream)


def test_class():
    @dataclass
    class Person:
        name: str
        age: int

    s = io.BytesIO()
    ps = Person("Alessio", 27)

    pk = Wrap(lambda x: Person(*x), lambda p: (p.name, p.age), ArgWrap(String(), Maybe(Uint8)))
    pk.pickle(ps, s)
    s.seek(0)
    print(s.getvalue())
    person = pk.unpickle(s)
    print(person[0])


def test_str():
    pu = String()
    bs = pu.pickle("Alessio", io.BytesIO(b''))
    bs.seek(0)
    print(bs.getvalue())
    name = pu.unpickle(bs)
    print(name[0])


def test_other():
    @dataclass
    class Person:
        name: str
        age: int = None

    s = io.BytesIO()
    ps = Person("Timna")

    pk = Wrap(lambda x: Person(*x), lambda p: (p.name, p.age), ArgWrap(String(), Maybe(Uint8)))
    pk.pickle(ps, s)
    s.seek(0)
    print(s.getvalue())
    person = pk.unpickle(s)
    print(person[0])


def test_kw_pickler():
    @dataclass
    class Person:
        name: str
        age: int = None

    s = io.BytesIO()
    ps = Person("Timna")
    p2 = Person("Timna", 26)

    pk = KWrap(Person, name=String(), age=Maybe(Uint8))
    pk.pickle(ps, s)
    s.seek(0)
    print(s.getvalue())
    person = pk.unpickle(s)
    print(person[0])

    s2 = io.BytesIO()
    pk.pickle(p2, s2)
    s2.seek(0)
    print(pk.unpickle(s2)[0])


def test_fixed_list():
    @dataclass
    class Person:
        name: str
        age: int = None

    s = io.BytesIO()
    ps = [Person("Timna"), Person("Simon", 20), Person("Alessio", 27)]

    pk = FixedList(KWrap(Person, name=String(), age=Maybe(Uint8)), 3)
    pk.pickle(ps, s)
    s.seek(0)
    print(pk.unpickle(s)[0])


def test_list():
    @dataclass
    class Person:
        name: str
        age: int = None

    s = io.BytesIO()
    ps = [Person("Timna"), Person("Simon", 20), Person("Alessio", 27)]

    pk = List(KWrap(Person, name=String(), age=Maybe(Uint8)))
    pk.pickle(ps, s)
    s.seek(0)
    print(pk.unpickle(s)[0])


test_class()
test_str()
test_other()
test_kw_pickler()
test_fixed_list()
test_list()
