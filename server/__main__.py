from requests import get

from flask import Flask
from click import group, option, argument
from bs4 import BeautifulSoup

from .google_image_search import search

DEFAULT_PORT = 8080


class Server:

    def __init__(self, port: int = DEFAULT_PORT):
        self.port = port

        self.app = Flask('mlook')

        self._init_movies()

    def _init_movies(self):
        @self.app.route('/movies')
        def movies():
            page = get('https://thepiratebay0.org/browse/201')
            bs = BeautifulSoup(page.text, 'html.parser')

            items = []

            for item in bs.find(id = 'searchResult').find_all('tr')[1:]:
                # print(item)

                links = item.find_all('a', {'class': 'detLink'})

                if len(links) < 1:
                    continue

                link = links[0]['href']

                magnet_links = item.find_all('a', {'title': 'Download this torrent using magnet'})

                if len(magnet_links) < 1:
                    continue

                magnet_link = magnet_links[0]['href']

                names = item.find_all('div', {'class': 'detName'})

                if len(names) < 1:
                    continue

                name = names[0].text

                items.append({'link': link, 'magnet-link': magnet_link, 'name': name})

                return search(name)

                # print(images)

                # if len(images) < 1:
                #     raise ValueError(f'No images found for query {name}')
                #     continue

                # print(images[0])

                # dd

                # # name_components = name.split('.', maxsplit = 2)

                # # if len(name_components) > 2:
                # #     print(link, magnet_link, ' '.join(name_components[:2]))
                # # else:
                # #     print(link, magnet_link, name)

            return {
                'items': items
            }

    def start(self):
        self.app.run(host = '0.0.0.0', port = self.port)


@group()
def main():
    pass


@main.command()
@option('--port', '-p', type = int, default = DEFAULT_PORT)
def start(port: int):
    Server(port).start()


@main.command()
@argument('query', type = str)
def search_images(query: str):
    print(search(query)[0])


if __name__ == '__main__':
    main()
