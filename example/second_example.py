
import os

from slack_bot import Application, Response, RoutersTable


app = Application(token=os.getenv('SLACK_TOKEN'))
table = RoutersTable()


@table.route('U123456')
def say_hello(request):
    return Response(request=request, text=f'Hi! {request.user}')


if __name__ == '__main__':
    app.run()
