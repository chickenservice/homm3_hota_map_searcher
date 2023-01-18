from h3map.show_my_maps.parser import Parser


class LossConditionReader:
    def __init__(self, stream):
        self.loss_condition = None
        self.loss_condition_type = None
        self._stream: Parser = stream
        self._loss_conditions = _loss_condition_readers

    def read(self):
        self.loss_condition_type = self._stream.uint8()
        if self.loss_condition_type == 255:
            self.loss_condition = StandardLossConditionReader(self._stream)
        else:
            self.loss_condition = self._loss_conditions[self.loss_condition_type](self._stream)

    def __str__(self):
        return str(self.loss_condition)


class StandardLossConditionReader:
    def __init__(self, stream):
        self._stream: Parser = stream

    def __str__(self):
        return "Standard loss condition"


class LoseSpecificTownReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()

    def __str__(self):
        return "Lose specific town"


class LoseSpecificHeroReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.x = self.parser.uint8()
        self.y = self.parser.uint8()
        self.z = self.parser.uint8()

    def __str__(self):
        return "Lose specific hero"


class TimeExpiresReader:
    def __init__(self, parser):
        self.parser = parser
        self._read()

    def _read(self):
        self.days = self.parser.uint16()

    def __str__(self):
        return "Time expires"


_loss_condition_readers = [
    LoseSpecificTownReader,
    LoseSpecificHeroReader,
    TimeExpiresReader,
]