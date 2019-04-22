
import os

from slack_bot import Application, RoutersTable


app = Application(token=os.getenv('SLACK_TOKEN'))
table = RoutersTable()


@table.route('U123456')
def say_hello(request):
    return f'Hi! {request}'


if __name__ == '__main__':
    app.run()
