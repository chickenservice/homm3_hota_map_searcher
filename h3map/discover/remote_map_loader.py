import requests


class UrlHtmlMapInfoLoader:
    def __init__(self, url):
        self.url = url

    def load(self, page=0):
        if page > 0:
            response = requests.get(self.url + "/?&limit={0}".format(page))
        else:
            response = requests.get(self.url)
        if response.ok:
            return response.text
        else:
            raise RuntimeError("Could not load map headers from {0}".format(self.url))


class FileHtmlMapInfoLoader:
    def __init__(self, path):
        self.path = path

    def load(self, page=0):
        path = self.path[:-5] + str(page) + ".html"
        if page >= 3:
            return ""
        with open(path, 'r', encoding='utf-8') as f:

            return f.read()
