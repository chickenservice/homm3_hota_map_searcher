from h3map.heroes3map.models import Hero, HeroInfo
from h3map.heroes3map._old.schema.schema import Schema


class HeroPropertiesSchema(Schema):
    def __init__(self, has_random_hero, main_custom_hero_id, **kwargs):
        super().__init__(Hero, **kwargs)
        self.has_random_hero = has_random_hero
        self.main_custom_hero_id = main_custom_hero_id

    def __call__(self, stream, **kwargs):
        random_hero = self.has_random_hero(stream)
        hero_type = self.main_custom_hero_id(stream)
        if hero_type != 255:
            super().__call__(stream)
        return HeroInfo(has_random_hero=random_hero, hero_type=hero_type)
