
import os

from slack_bot import Application, Response, Route


def say_hello(request):
    return Response(request=request, text=f'Hi! {request.user}')


if __name__ == '__main__':
    app = Application(token=os.getenv('SLACK_TOKEN'))
    app.add_routes([
        Route(route='Hello', handler=say_hello),
    ])
    app.run()
