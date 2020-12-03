import abc


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
            print(header)
