import os

from slack_bot import Application, Response


TOKEN = os.getenv('SLACK_TOKEN')


app = Application(token=TOKEN)


@app.route('hello', channels=[], users=[])
def main(request):
    return Response(request=request, text=f'Hi! {request.user}')


if __name__ == '__main__':
    app.run()
