import json
import os
import time
from typing import List

from slackclient import SlackClient

from slack_bot.models import Message, Response
from slack_bot.routes import Routers, Route


RTM_READ_DELAY = int(os.getenv('RTM_READ_DELAY', 1))


class Application:

    def __init__(self, token):
        self._token = token
        self._client = None
        self._bot_id = None
        self._routers = Routers()

    @property
    def bot_id(self) -> str:
        if not self._bot_id:
            self._bot_id = self.client.api_call("auth.test")["user_id"]
        return self._bot_id

    @property
    def client(self) -> SlackClient:
        if not self._client:
            self._client = self._client_connected()
        return self._client

    @client.setter
    def client(self, custom_client):
        """
        For easy tests only, add mocked client
        :param SlackClient custom_client: For example MagicMock()
        """
        self._client = custom_client

    def _client_connected(self) -> SlackClient:
        sc = SlackClient(token=self._token)
        if sc.rtm_connect():
            return sc
        raise Exception('Validate your token')

    def _send(self, response: Response) -> bool:
        """
        Response required attributes:
            channel="C1234567890"   Channel, where message wrote
            text="Hello world"	    Text, message to response

        Response optional attributes:
            username="MyBotName"
            as_user=True
            attachments=[{"pretext": "pre-hello", "text": "text-world"}]
            blocks=[{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}]
            icon_emoji=":wink:"
            icon_url="http://lorempixel.com/48/48"
            link_names=True
            mrkdwn=False
            parse='full'
            reply_broadcast=True
            thread_ts='1234567890.123456'
            unfurl_links=True
            unfurl_media=False

        More info: https://api.slack.com/methods/chat.postMessage
        api_call(
            method='chat.postMessage',
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

    def route(self, route, channels=None, users=None):
        """
        Decorator add some bot actions if route wen equal message
        Usage:

            table = RoutersTable()

            @table.route('hello')
            def some_bot_action(request):
                return Response(request=request, text='Hi!')

        :param str route: target message in slack
        :param list[str] channels: only for subscribe channels
        :param list[str] users: only for subscribe users
        """
        def wrapper(handler):
            self._routers.table.add_route(route, handler, channels, users)
            return handler
        return wrapper

    def add_routes(self, routes: List[Route]):
        """
        Add handlers for all bot actions
        Usage:
            table = RoutersTable()
            table.add_routes([
                Route('hello', say_hello_handler),
                Route('how do you do?', answer_handler),
            ])

        :param list[Route] routes:
        :return: list[Route]
        """
        self._routers.table.add_routes(routes)

    def _process_message(self, raw_msg) -> bool:
        if not raw_msg:
            return False

        # parse message and find need handler
        msg = Message(raw_msg)
        route = self._routers.find_route(msg)
        if route is None:
            return False

        # send response to slack
        response = route.handler(msg)
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
