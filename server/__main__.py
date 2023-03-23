from json import load
from time import time, sleep

from requests import get

from flask import Flask
from click import group, option, argument
from bs4 import BeautifulSoup
from flask_cors import CORS

from .google_image_search import search

DEFAULT_PORT = 8080
MOVIES_RESPONSE_EXAMPLE_PATH = 'assets/movies-response-example.json'


def get_single_link(images):
    if images is None or len(images) == 0:
        return None

    for image in images:
        if image['source'] == 'IMDb':
            return image['original']

    return images[0]['original']


class Server:

    def __init__(self, port: int = DEFAULT_PORT, min_movies_query_interval: int = 60):
        self.port = port

        self.app = app = Flask('mlook')
        CORS(app)

        self._init_movies()
        self._init_movies_example()

        self.last_query_timestamp = None

        self.min_movies_query_interval = min_movies_query_interval

    def _init_movies(self):
        @self.app.route('/movies/<page>/<section>')
        def movies(page: int, section: int):

            if self.last_query_timestamp is not None:
                if (diff := time() - self.last_query_timestamp) < self.min_movies_query_interval:
                    remaining_time = self.min_movies_query_interval - diff
                    print(f'Waiting for {remaining_time} more seconds to avoid captcha')
                    sleep(remaining_time)
                    print('finished waiting')

            page = get(f'https://thepiratebay0.org/browse/201/{page}/{section}')
            # page = get('https://thepiratebay0.org/browse/201')
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

                images, html = search(name)

                if len(images) < 1:
                    self.last_query_timestamp = time()

                    return html
                    # raise ValueError(f'No images found for query {name}')
                    # continue

                items.append({'details': link, 'magnet': magnet_link, 'name': name, 'poster': get_single_link(images)})

                # name_components = name.split('.', maxsplit = 2)

                # if len(name_components) > 2:
                #     print(link, magnet_link, ' '.join(name_components[:2]))
                # else:
                #     print(link, magnet_link, name)

            self.last_query_timestamp = time()

            return {
                'items': items
            }

    def _init_movies_example(self):
        @self.app.route('/movies-example/<page>/<section>')
        def movies_example(page: int, section: int):
            with open(MOVIES_RESPONSE_EXAMPLE_PATH, 'r', encoding = 'utf-8') as file:
                return load(file)

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
