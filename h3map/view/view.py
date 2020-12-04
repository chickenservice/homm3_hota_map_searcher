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
        return self.header.metadata.description.summary


class MapSizeView:
    _sizes = {
        144: "XL",
        72: "L",
        36: "M",
        18: "S",
    }

    def __init__(self, header):
        self.header = header

    def render(self):
        size = self.header.properties.size
        return self._sizes[size]

