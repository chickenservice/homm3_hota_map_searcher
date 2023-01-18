import logging
import struct

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def Uint8(stream):
    return struct.unpack('B', stream.read(1))[0]


def Uint16(stream):
    return struct.unpack('H', stream.read(2))[0]


def Uint32(stream):
    return struct.unpack('i', stream.read(4))[0]


def Bool(stream):
    return struct.unpack('?', stream.read(1))[0]


def _get_format_string(repetitions, character):
    return str(repetitions) + character


def String(stream):
    size = Uint32(stream)
    if size > 500000:
        raise ValueError("Size too big for string.")
    pattern = _get_format_string(size, 's')

    return struct.unpack(pattern, stream.read(size))[0]


def Uchar(stream):
    return struct.unpack('B', stream.read(1))[0]


class Schema:
    def __init__(self, cls, **kwargs):
        self._attrs = kwargs
        self._blueprint = cls

    def __call__(self, stream):
        LOGGER.info(self)
        try:
            return {k: v(stream) for k, v in self._attrs.items()}
        except AssertionError:
            return None

    def __repr__(self):
        return f"Schema(name={self._blueprint.__name__}, attr={', attr='.join(self._attrs)})"


class Transform(Schema):
    def __init__(self, clbk, **kwargs):
        super().__init__(dict, **kwargs)
        self._clbk = clbk

    def __call__(self, stream, **kwargs):
        vals = super().__call__(stream)
        return self._clbk(*vals.values())


class If(Schema):
    def __init__(self, condition, **kwargs):
        super().__init__(dict, **kwargs)
        self._condition = condition

    def __call__(self, stream):
        vals = super().__call__(stream)
        if condition := self._condition(stream, *vals):
            return condition, *vals
        else:
            raise AssertionError


class Select(Schema):
    def __init__(self, value, **kwargs):
        super().__init__(dict, **kwargs)
        self._value = value

    def __call__(self, stream, **kwargs):
        ctx = super().__call__(stream)
        return ctx[self._value]


class Repeat(Schema):
    def __init__(self, schema, start, stop, **kwargs):
        super().__init__(dict, **kwargs)
        self._start = start
        self._stop = stop
        self._schema = schema

    def __call__(self, stream, **kwargs):
        vals = []
        for i in range(self._start(stream), self._stop(stream)):
            vals.append(self._schema(stream))

        return vals


def Constant(c): return lambda x: c
