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
