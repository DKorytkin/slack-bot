import os

from slack_bot import Application


app = Application(os.getenv('SLACK_TOKEN'))


@app.route("Hello")
def say_hello(request):
    return f"Hi, {request.user}"


if __name__ == "__main__":
    app.run()
