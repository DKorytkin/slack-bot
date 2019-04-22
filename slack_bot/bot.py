import os
import time

from slackclient import SlackClient

from slack_bot.routes import Routers


RTM_READ_DELAY = os.getenv('RTM_READ_DELAY', 1)
TOKEN = os.getenv('SLACK_TOKEN')


def send(sc: SlackClient):
    sc.api_call(
        'chat.postMessage',
        channel='#general',
        text='try it',
        username='Mario',
        icon_emoji=':mario:'
    )


def client_connected(token: str) -> SlackClient:
    sc = SlackClient(token=token)
    if sc.rtm_connect():
        return sc
    raise Exception('Validate your token')


class Message:

    def __init__(self, raw):
        self._raw_message = raw

    @property
    def text(self):
        return 'Hello'

    @property
    def user(self):
        return 'Name user'


class Response:

    def __init__(self, text):
        self.text = text


class Application:

    def __init__(self, token):
        self._token = token
        self._client = None
        self._bot_id = None
        self._routers = Routers()

    @property
    def client(self):
        if not self._client:
            self._client = client_connected(token=self._token)
        return self._client

    def check(self):
        self._bot_id = self.client.api_call("auth.test")["user_id"]
        return self._bot_id

    def route(self, rout, channels=None, users=None):
        """
        decorator
        """
        def wrapper(handler):
            self._routers.table.add_route(rout, handler, channels, users)
            return handler
        return wrapper

    def add_routes(self, routes: list):
        raise NotImplementedError

    def _process_message(self, raw_msg):
        if not raw_msg:
            return False

        # parse
        msg = Message(raw_msg)
        handler = self._routers.find_handler(msg.text)
        if handler is None:
            return False

        # send
        handler(msg)
        send(self.client)
        return True

    def run(self):
        while True:
            raw_msg = self.client.rtm_read()
            self._process_message(raw_msg)
            # all action done
            time.sleep(RTM_READ_DELAY)
