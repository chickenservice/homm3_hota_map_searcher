import chardet


def _decode(string):
    encoding = chardet.detect(string)['encoding'] or 'utf-8'
    return string.decode(encoding)


class Metadata:
    def __init__(self, stream):
        self.diff = None
        self.max_level = None
        self.description = None
        self.name = None
        self.two_level = None
        self.height = None
        self.any_players = None
        self._stream = stream

    def read(self):
        self.any_players = self._stream.bool()
        self.height = self._stream.uint32()
        self.two_level = self._stream.bool()
        self.name = _decode(self._stream.string())
        self.description = _decode(self._stream.string())
        self.diff = self._stream.uint8()
        self.max_level = self._stream.uint8()
        #if self.read_version().version == 14:
        #    self.max_level = 4

    def __repr__(self):
        return f"Any players: {self.any_players}\n" \
               f"Size: {self.height}\n" \
               f"Two levels: {self.two_level}\n" \
               f"Name: {self.name}\n" \
               f"Description: {self.description}\n" \
               f"Difficulty: {self.diff}\n" \
               f"Level cap: {self.max_level}\n"


class AiTactic:
    def __init__(self, stream):
        self.ai_tactic = None
        self.parser = stream

    def read(self):
        self.ai_tactic = self.parser.uint8()
        _ = self.parser.uint8()

    def __repr__(self):
        return f"{self.ai_tactic}"


class FactionInfo:
    def __init__(self, stream, towns=None):
        self.is_faction_random = None
        self.allowed_factions = None
        self.allowed = None
        self.total = None
        self.parser = stream
        self._towns = towns if towns else []

    def read(self):
        self.total = self.parser.uint8()
        self.allowed = self.total + self.parser.uint8() * 256
        self.allowed_factions = self._get_allowed_factions()
        self.is_faction_random = self.parser.bool()

    def _get_allowed_factions(self):
        return [faction for i, faction in enumerate(self._towns[:self.total]) if (self.allowed & (1 << i))]

    def __repr__(self):
        return "\n".join(self.allowed_factions)


class TownInfo:
    def __init__(self, stream):
        self.z = None
        self.y = None
        self.x = None
        self.b = None
        self.a = None
        self.has_main_town = None
        self.parser = stream

    def read(self):
        self.has_main_town = self.parser.bool()
        if self.has_main_town:
            self.a = self.parser.bool()
            self.b = self.parser.bool()
            self.x = self.parser.uint8()
            self.y = self.parser.uint8()
            self.z = self.parser.uint8()

    def __repr__(self):
        return f"Has main town: {self.has_main_town}"


class HeroProperties:
    def __init__(self, stream):
        self.name = None
        self._id = None
        self.main_custom_hero_id = None
        self.has_random_hero = None
        self.parser = stream

    def read(self):
        self.has_random_hero = self.parser.bool()
        self.main_custom_hero_id = self.parser.uint8()
        if self.main_custom_hero_id != 255:
            self._id = self.parser.uint8()
            self.name = self.parser.string()

    def __repr__(self):
        return f"Random hero: {self.has_random_hero}\nHero ID: {self.main_custom_hero_id}"


class Hero:
    def __init__(self, stream):
        self.name = None
        self._id = None
        self.parser = stream

    def read(self):
        self._id = self.parser.uint8()
        self.name = self.parser.string()

    def __repr__(self):
        return f"Id: {self._id}\nName: {self.name}"


class HeroesBelongingToPlayers:
    def __init__(self, stream):
        self.hero_count = None
        self._heroes = None
        self.parser = stream

    def read(self):
        self._heroes = []
        self.parser.uint8()
        self.hero_count = self.parser.uint8()
        self.parser.skip(3)
        for i in range(0, self.hero_count):
            self._heroes.append(Hero(self.parser))

    def __repr__(self):
        return "\n".join([repr(hero) for hero in self._heroes])


class PlayerInfo:
    def __init__(self, stream, number, ai_tactic=None, faction_info=None, town_info=None, hero_props=None, heroes=None, skip=13):
        self.can_computer_play = None
        self.can_human_play = None
        self.parser = stream
        self.number = number
        self.ai_tactic = ai_tactic
        self.faction_info = faction_info
        self.town_info = town_info
        self.hero_properties = hero_props
        self.heroes = heroes
        self._skip = skip

    def read(self):
        self.can_human_play = self.parser.bool()
        self.can_computer_play = self.parser.bool()
        if self._not_playable():
            self.parser.skip(self._skip)
        else:
            self.ai_tactic.read()
            self.faction_info.read()
            self.town_info.read()
            self.hero_properties.read()
            self.heroes.read()

    def _not_playable(self):
        return not(self.can_human_play or self.can_computer_play)

    def __repr__(self):
        return f"Player {self.number}\nAI: {self.ai_tactic}\nFactions:{self.faction_info}\nTowns:{self.town_info}\nHero props:{self.hero_properties}\n:Heroes{self.heroes}\n\n"


class PlayerInfos:
    def __init__(self, player_info=None):
        self.players = player_info

    def read(self):
        for player_number in self.players:
            player_number.read()

    def __repr__(self):
        return "".join([repr(player) for player in self.players])


class Teams:
    def __init__(self, stream):
        self.teams = []
        self.number_of_teams = None
        self._stream = stream

    def read(self):
        self.number_of_teams = self._stream.uint8()
        if self.number_of_teams > 0:
            for player in range(0, 8):
                team_id = self._stream.uint8()
                if team_id == 255:
                    team_id = 7
                self.teams.append(team_id)
        else:
            for player in range(0, 8):
                self.teams.append(player)

    def __repr__(self):
        return f"{self.teams}"


class AllowedHeroes:
    def __init__(self, stream, heroes=None):
        self.allowed = None
        self._stream = stream
        self._heroes = heroes if heroes else []
        self._number_of_heroes = len(self._heroes)

    def read(self):
        negate = False
        allowed_heroes = [True] * self._number_of_heroes
        for byte in range(0, 20):
            allowed = self._stream.uint8()
            for bit in range(0, 8):
                if byte * 8 + bit < self._number_of_heroes:
                    flag = allowed & (1 << bit)
                    if (negate & flag) or ((not negate) & (not flag)):
                        allowed_heroes.insert(byte * 8 + bit, False)

        self.allowed = [hero for i, hero in enumerate(self._heroes) if allowed_heroes[i]]

    def __repr__(self):
        return f"{self.allowed}"


class Header:
    def __init__(self, metadata=None, player_infos=None, winning_condition=None, loss_condition=None, teams=None, allowed_heroes=None):
        self.metadata = metadata
        self.player_infos = player_infos
        self.winning_condition = winning_condition
        self.loss_condition = loss_condition
        self.teams = teams
        self.allowed_heroes = allowed_heroes

    def read(self):
        self.metadata.read()
        self.player_infos.read()
        self.winning_condition.read()
        self.loss_condition.read()
        self.teams.read()
        self.allowed_heroes.read()

    def __repr__(self):
        return f"{self.metadata}\n{self.player_infos}\n{self.winning_condition}\n{self.loss_condition}\n{self.teams}\n{self.allowed_heroes}"
