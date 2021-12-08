import math

from bs4 import BeautifulSoup

from h3map.header.models import Header, Metadata, TeamSetup, Description, PlayerInfo


class DiscoverMaps4Heroes:
    items_per_page = 10

    def __init__(self, loader):
        self.loader = loader
        self.current_page = 0
        self.items_loaded = 0

    def list_maps(self, requested=0):
        items = []
        pages = math.ceil(requested / self.items_per_page)
        if self.items_loaded + requested <= self.current_page * self.items_per_page:
            return []

        for _page in range(0, pages):
            page = _page + self.current_page

            html = self.loader.load(page=page)
            if not len(html):
                continue

            self.current_page += 1
            self.items_loaded += self.items_per_page
            items += self._get_maps(html)

        return items

    def _get_maps(self, html):
        parsed = BeautifulSoup(html, 'html.parser')
        maps = parsed.find_all(attrs={"class": "maps_table"})
        headers = []
        for info in zip(maps[::2], maps[1::2]):
            metadata: Metadata = self._get_metadata(info[0])
            team_setup: TeamSetup = self._get_team_info(info[1])
            player_info: PlayerInfo = self._get_player_info(info[1])
            headers.append(Header(metadata, [player_info], team_setup, [], []))

        return headers

    def _get_metadata(self, html_map):
        name = html_map.b.text if html_map.b else ""
        summary = ""
        description = Description(name, summary)
        return Metadata(0, None, description, None, thumbnail=html_map.img['src'])

    def _get_team_info(self, html_map):
        return TeamSetup(0, [])

    def _get_player_info(self, html_map):
        return PlayerInfo(None, None, None, None, None, None)
