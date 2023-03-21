from flask import Flask
from click import group, option

DEFAULT_PORT = 8080


class Server:

    def __init__(self, port: int = DEFAULT_PORT):
        self.port = port

        self.app = Flask('mlook')

        self._init_movies()

    def _init_movies(self):
        @self.app.route('/movies')
        def movies():
            return 'Foo bar'

    def start(self):
        self.app.run(host = '0.0.0.0', port = self.port)


@group()
def main():
    pass


@main.command()
@option('--port', '-p', type = int, default = DEFAULT_PORT)
def start(port: int):
    Server(port).start()


if __name__ == '__main__':
    main()
