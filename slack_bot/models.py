from typing import List


class Message:

    def __init__(self, raw: List[dict]):
        self._raw = raw
        self._raw_message = raw[0] if len(raw) == 1 and isinstance(raw, list) else raw
        self._match_info = {}

    @property
    def match_info(self) -> dict:
        return self._match_info

    @match_info.setter
    def match_info(self, info: dict):
        if not isinstance(info, dict):
            raise TypeError('Info must be dict')
        self._match_info = info

    @match_info.deleter
    def match_info(self):
        self._match_info = {}

    @property
    def type(self) -> str:
        return self._raw_message.get('type')

    @property
    def subtype(self) -> str:
        return self._raw_message.get('subtype')

    @property
    def client_msg_id(self) -> str:
        return self._raw_message.get('client_msg_id')

    @property
    def team(self) -> str:
        return self._raw_message.get('team')

    @property
    def channel(self) -> str:
        return self._raw_message.get('channel')

    @property
    def text(self) -> str:
        return self._raw_message.get('text')

    @property
    def user(self) -> str:
        return self._raw_message.get('user')

    @property
    def event_ts(self) -> str:
        return self._raw_message.get('event_ts')

    @property
    def ts(self) -> str:
        return self._raw_message.get('ts')

    def is_type_message(self) -> bool:
        return bool('message' == self.type)

    def is_bot_message(self) -> bool:
        return bool('bot_message' == self.subtype or self._raw_message.get('bot_id'))

    def is_suppress_notification(self) -> bool:
        return bool(self._raw_message.get('suppress_notification'))


class Response:

    def __init__(self, request: Message, text: str, method: str = 'chat.postMessage', **kwargs):
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

        Example:
            method='chat.postMessage',
            channel='#general',
            text='Hi!',
            username='BotName',
            icon_emoji=':wink:'

        :param Message request:
        :param str text:
        :param str method:
        :param kwargs:
        """
        self._request = request
        self.text = text
        self.method = method
        self.kw = kwargs

    def _base(self) -> dict:
        d = {
            'method': self.method,
            'text': self.text,
            'channel': self._request.channel,
            'us_user': True,
            'icon_emoji': ':ghost:'
        }
        return d

    def to_dict(self) -> dict:
        data = self._base()
        data.update(self.kw)
        return data
