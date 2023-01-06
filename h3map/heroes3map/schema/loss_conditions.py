from h3map.heroes3map.loss_conditions import StandardLossCondition, LoseSpecificTown, LoseSpecificHero, TimeExpires
from h3map.heroes3map.schema.schema import Schema, Uint8, Uint16


class LossCondition(Schema):
    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)
        self._loss_conditions = _loss_condition_readers

    def __call__(self, stream, **kwargs):
        self.loss_condition_type = self._attrs["condition"](stream)
        if self.loss_condition_type == 255:
            return StandardLossCondition(255)
        else:
            return self._loss_conditions[self.loss_condition_type](stream)


lose_specific_town = Schema(
    LoseSpecificTown,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)


lose_specific_hero = Schema(
    LoseSpecificHero,
    x=Uint8,
    y=Uint8,
    z=Uint8,
)

time_expires = Schema(
    TimeExpires,
    days=Uint16
)

_loss_condition_readers = [
    lose_specific_town,
    lose_specific_hero,
    time_expires,
]