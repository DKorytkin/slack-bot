
import os

from slack_bot import Application, Route


def say_hello(request):
    return f'Hi! {request}'


if __name__ == '__main__':
    app = Application(token=os.getenv('SLACK_TOKEN'))
    app.add_routes([
        Route(rout='Hello', handler=say_hello),
    ])
    app.run()
