
import os

from slack_bot import Application, Response, RoutersTable


table = RoutersTable()


@table.route('hello')
def say_hello(request):
    return Response(request=request, text=f'Hi! {request.user}')


if __name__ == '__main__':
    app = Application(token=os.getenv('SLACK_TOKEN'))
    app.run()
