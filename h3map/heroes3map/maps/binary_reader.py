import struct
from typing import BinaryIO


def _get_format_string(repetitions, character):
    return str(repetitions) + character


class BinaryReader:
    def __init__(self, buffer: BinaryIO):
        self._buffer: BinaryIO = buffer

    def uint8(self):
        return struct.unpack('B', self._buffer.read(1))[0]

    def uint16(self):
        return struct.unpack('H', self._buffer.read(2))[0]

    def uint32(self):
        return struct.unpack('I', self._buffer.read(4))[0]

    def bool(self):
        return struct.unpack('?', self._buffer.read(1))[0]

    def uchar(self):
        return struct.unpack('B', self._buffer.read(1))[0]

    def string(self):
        size = self.uint32()
        if size > 500000:
            raise ValueError("Size too big for string.")
        pattern = _get_format_string(size, 's')

        return struct.unpack(pattern, self._buffer.read(size))[0]

    def skip(self, delta):
        self._buffer.read(delta)
