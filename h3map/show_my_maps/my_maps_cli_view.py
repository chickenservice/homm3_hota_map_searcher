import abc

import cli_ui


class Cli(abc.ABC):
    @abc.abstractmethod
    def show(self):
        raise NotImplemented("Implement a concrete view.")


class List(Cli):
    def __init__(self, maps):
        self.maps = maps

    def show(self):
        for name in self.maps.names():
            print(name.render())


class ListDetailed(Cli):
    def __init__(self, maps):
        self.maps = maps

    def show(self):
        names = self.maps.names()
        summaries = self.maps.descriptions()

        for n, s in zip(names, summaries):
            cli_ui.info_section(n.render())
            cli_ui.info(s.render())
            print('\n')



class MapsView:
    def __init__(self, maps):
        self.maps = maps

    def names(self):
        return [NameView(name) for name in self.maps]

    def descriptions(self, index=None):
        descriptions = [DescriptionView(name) for name in self.maps]
        if index is not None:
            return descriptions[index]

        return descriptions

    def all(self):
        return self.maps

    def update(self, maps):
        for mp in maps.maps:
            self.maps.append(mp)


class NameView:
    def __init__(self, header):
        self.header = header

    def render(self):
        return self.header.metadata.description.name


class DescriptionView:
    def __init__(self, header):
        self.header = header

    def render(self):
        summary = self.header.metadata.description.summary
        size = MapSizeView(self.header).render()
        number_of_teams = self.header.teams.number_of_teams

        return "Summary: {0}\n\nMap size: {1}\n\nNumber of teams: {2}\n\n".format(summary, size, number_of_teams)


class MapSizeView:
    _sizes = {
        144: "XL",
        108: "L",
        72: "M",
        36: "S",
    }

    def __init__(self, header):
        self.header = header

    def render(self):
        size = self.header.metadata.properties.size
        return self._sizes[size]

