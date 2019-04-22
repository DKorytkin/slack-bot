import json
import os
import time

from slackclient import SlackClient

from slack_bot.models import Message, Response
from slack_bot.routes import Routers


RTM_READ_DELAY = os.getenv('RTM_READ_DELAY', 1)


class Application:

    def __init__(self, token):
        self._token = token
        self._client = None
        self._bot_id = None
        self._routers = Routers()

    @property
    def client(self):
        if not self._client:
            self._client = self._client_connected()
        return self._client

    def _client_connected(self) -> SlackClient:
        sc = SlackClient(token=self._token)
        if sc.rtm_connect():
            return sc
        raise Exception('Validate your token')

    def _send(self, response: Response) -> bool:
        """
        sc.api_call(
            'chat.postMessage',
            channel='#general',
            text='try it',
            username='Mario',
            icon_emoji=':mario:'
        )
        :param Response response:
        :return: bool
        """
        self.client.api_call(**response.to_dict())
        return True

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
        raise self._routers.table.add_routes(routes)

    def _process_message(self, raw_msg):
        if not raw_msg:
            return False

        # parse message and find need handler
        msg = Message(raw_msg)
        handler = self._routers.find_handler(msg.text)
        if handler is None:
            return False

        # send response to slack
        response = handler(msg)
        if not isinstance(response, Response):
            raise TypeError('Handler must be return instance Response class')
        return self._send(response)

    def run(self):
        while True:
            raw_msg = self.client.rtm_read()
            print(json.dumps(raw_msg))
            self._process_message(raw_msg)
            # all action done
            time.sleep(RTM_READ_DELAY)
