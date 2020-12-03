import abc

import cli_ui


class CliView(abc.ABC):
    @abc.abstractmethod
    def show(self):
        raise NotImplemented("Implement a concrete view.")


class List(CliView):
    def show(self, headers):
        for header in headers:
            print(header.metadata.description.name)


class ListDetailed(CliView):
    def show(self, headers):
        for header in headers:
            cli_ui.info_section(header.metadata.description.name.decode('latin-1'))
            cli_ui.info(header.metadata.description.summary.decode('latin-1'))
            print('\n')
            cli_ui.info(header.teams)
            print('\n\n')
