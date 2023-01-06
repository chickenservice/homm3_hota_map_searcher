import chardet

from h3map.heroes3map.header.loss_conditions import LossConditionReader
from h3map.heroes3map.header.winning_conditions import WinningConditionReader


def _decode(string):
    encoding = chardet.detect(string)['encoding'] or 'utf-8'
    return string.decode(encoding)


class Metadata:
    def __init__(self, stream):
        self._stream = stream
        self._read()

    def _read(self):
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
        self.parser = stream
        self._read()

    def _read(self):
        self.ai_tactic = self.parser.uint8()
        _ = self.parser.uint8()

    def __repr__(self):
        return f"{self.ai_tactic}"


class FactionInfo:
    def __init__(self, stream, towns=None):
        self.parser = stream
        self._towns = towns if towns else []
        self._read()

    def _read(self):
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
        self.parser = stream
        self._read()

    def _read(self):
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
        self.parser = stream
        self._read()

    def _read(self):
        self.has_random_hero = self.parser.bool()
        self.main_custom_hero_id = self.parser.uint8()
        if self.main_custom_hero_id != 255:
            self._id = self.parser.uint8()
            self.name = self.parser.string()

    def __repr__(self):
        return f"Random hero: {self.has_random_hero}\nHero ID: {self.main_custom_hero_id}"


class Hero:
    def __init__(self, stream):
        self.parser = stream
        self._read()

    def _read(self):
        self._id = self.parser.uint8()
        self.name = self.parser.string()

    def __repr__(self):
        return f"Id: {self._id}\nName: {self.name}"


class HeroesBelongingToPlayers:
    def __init__(self, stream):
        self.parser = stream
        self._read()

    def _read(self):
        self._heroes = []
        self.parser.uint8()
        self.hero_count = self.parser.uint8()
        self.parser.skip(3)
        for i in range(0, self.hero_count):
            self._heroes.append(Hero(self.parser))

    def __repr__(self):
        return "\n".join([repr(hero) for hero in self._heroes])


class PlayerInfo:
    def __init__(self, stream, number):
        self.parser = stream
        self.number = number
        self._read()

    def _read(self):
        self.can_human_play = self.parser.bool()
        self.can_computer_play = self.parser.bool()
        if self._not_playable():
            self.parser.skip(13)
        else:
            self.ai_tactic = AiTactic(self.parser)
            self.faction_info = FactionInfo(self.parser)
            self.town_info = TownInfo(self.parser)
            self.hero_properties = HeroProperties(self.parser)
            self.heroes = HeroesBelongingToPlayers(self.parser)

    def _not_playable(self):
        return not(self.can_human_play or self.can_computer_play)

    def __repr__(self):
        return f"Player {self.number}\nAI: {self.ai_tactic}\nFactions:{self.faction_info}\nTowns:{self.town_info}\nHero props:{self.hero_properties}\n:Heroes{self.heroes}\n\n"


class PlayerInfos:
    def __init__(self, stream):
        self._stream = stream
        self._read()

    def _read(self):
        self.players = []
        for player_number in range(1, 9):
            self.players.append(PlayerInfo(self._stream, player_number))

    def __repr__(self):
        return "".join([repr(player) for player in self.players])


class Teams:
    def __init__(self, stream):
        self._stream = stream
        self._read()

    def _read(self):
        self.number_of_teams = self._stream.uint8()
        self.teams = []
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
        self._stream = stream
        self._heroes = heroes if heroes else []
        self._number_of_heroes = len(self._heroes)
        self._read()

    def _read(self):
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
    def __init__(self, stream, metadata=None, player_infos=None, winning_condition=None, loss_condition=None, teams=None, allowed_heroes=None):
        self._stream = stream
        self._read()

    def _read(self):
        self.metadata = Metadata(self._stream)
        self.player_infos = PlayerInfos(self._stream)
        self.winning_condition = WinningConditionReader(self._stream)
        self.loss_condition = LossConditionReader(self._stream)
        self.teams = Teams(self._stream)
        self.allowed_heroes = AllowedHeroes(self._stream)

    def __repr__(self):
        return f"{self.metadata}\n{self.player_infos}\n{self.winning_condition}\n{self.loss_condition}\n{self.teams}\n{self.allowed_heroes}"
