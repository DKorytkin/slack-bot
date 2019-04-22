import os

from slack_bot import Application


TOKEN = os.getenv('SLACK_TOKEN')


app = Application(token=TOKEN)


@app.route('hello', channels=[], users=[])
def main(request):
    return f'Hi! {request.user}'


if __name__ == '__main__':
    app.run()
