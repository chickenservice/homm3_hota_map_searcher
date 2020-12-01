import struct


class Parser:
    def __init__(self, buffer):
        self.buffer = buffer
        self.current = 0

    def _next(self, size):
        start = self.current
        stop = start + size
        self.current = stop

        return start, stop

    def _get_format_string(self, repetitions, character):
        return str(repetitions) + character

    def uint8(self):
        start, stop = self._next(1)
        return struct.unpack('B', self.buffer[start:stop])[0]

    def uint16(self):
        start, stop = self._next(4)
        return struct.unpack('I', self.buffer[start:stop])[0]

    def uint32(self):
        start, stop = self._next(4)
        return struct.unpack('I', self.buffer[start:stop])[0]

    def bool(self):
        start, stop = self._next(1)
        return struct.unpack('?', self.buffer[start:stop])[0]

    def uchar(self):
        start, stop = self._next(1)
        return struct.unpack('B', self.buffer[start:stop])[0]

    def string(self):
        size = self.uint32()
        if size > 500000:
            raise ValueError("Size too big for string.")
        start, stop = self._next(size)
        pattern = self._get_format_string(size, 's')

        return struct.unpack(pattern, self.buffer[start:stop])[0]

    def skip(self, delta):
        self.current += min(len(self.buffer) - self.current, delta);
