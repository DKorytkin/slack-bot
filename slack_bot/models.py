from typing import List


class Message:

    def __init__(self, raw: List[dict]):
        self._raw = raw
        self._raw_message = raw[0] if len(raw) == 1 and isinstance(raw, list) else raw
        self._match_info = {}
        self._info = None

    def __str__(self):
        return (
            f'<Message {self.type} '
            f'user={self.user_id} '
            f'channel={self.channel} '
            f'info={self._match_info}>'
        )

    def __repr__(self):
        return self.__str__()

    @property
    def _message(self):
        return self._raw_message.get('message', {})

    @property
    def info(self) -> dict:
        return self._info

    @info.setter
    def info(self, info: dict):
        if not isinstance(info, (tuple, list, set)):
            raise TypeError('Info must be one of (tuple, list, set)')
        self._info = info

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
        msg_id = self._raw_message.get('client_msg_id')
        if self.is_message_changed() and msg_id is None:
            msg_id = self._message.get('client_msg_id')
        return msg_id

    @property
    def team(self) -> str:
        return self._raw_message.get('team')

    @property
    def channel(self) -> str:
        return self._raw_message.get('channel')

    @property
    def text(self) -> str:
        msg = self._raw_message.get('text')
        if self.is_message_changed() and not msg:
            msg = self._message.get('text')
        return msg

    @property
    def user_id(self) -> str:
        user = self._raw_message.get('user')
        if self.is_message_changed() and user is None:
            user = self._message.get('user')
        return user

    @property
    def user(self):
        return f'<@{self.user_id}>'

    @property
    def event_ts(self) -> str:
        return self._raw_message.get('event_ts')

    @property
    def ts(self) -> str:
        return self._raw_message.get('ts')

    @property
    def thread_ts(self) -> str:
        return self._raw_message.get('thread_ts')

    def is_message_changed(self) -> bool:
        return bool('message_changed' == self.subtype)

    def is_type_message(self) -> bool:
        return bool('message' == self.type)

    def is_bot_message(self) -> bool:
        if 'bot_message' == self.subtype:
            return True
        return bool(self._raw_message.get('bot_id'))

    def is_suppress_notification(self) -> bool:
        return bool(self._raw_message.get('suppress_notification'))


class Response:

    def __init__(
            self,
            request: Message,
            text: str,
            method: str = 'chat.postMessage',
            thread_reply: bool = False,
            **kwargs
    ):
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
        :param bool thread_reply:
        :param kwargs:
        """
        self._request = request
        self.text = text
        self.method = method
        self.kw = kwargs
        self.thread_reply = thread_reply

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'<Response method={self.method} reply={self.thread_reply}, kw={self.kw}>'

    def _base(self) -> dict:
        d = {
            'method': self.method,
            'text': self.text,
            'channel': self._request.channel,
            'as_user': True,
            'icon_emoji': ':ghost:'
        }
        return d

    def to_dict(self) -> dict:
        data = self._base()
        data.update(self.kw)
        if self.thread_reply:
            data.update({'thread_ts': self._request.thread_ts or self._request.ts})
        return data
