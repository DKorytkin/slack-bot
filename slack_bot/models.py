
class Message:

    def __init__(self, raw):
        self._raw = raw
        self._raw_message = raw[0] if len(raw) == 1 and isinstance(raw, list) else raw

    @property
    def type(self):
        return self._raw_message.get('type')

    @property
    def subtype(self):
        return self._raw_message.get('subtype')

    @property
    def client_msg_id(self):
        return self._raw_message.get('client_msg_id')

    @property
    def team(self):
        return self._raw_message.get('team')

    @property
    def channel(self):
        return self._raw_message.get('channel')

    @property
    def text(self):
        return self._raw_message.get('text')

    @property
    def user(self):
        return self._raw_message.get('user')

    @property
    def event_ts(self):
        return self._raw_message.get('event_ts')

    @property
    def ts(self):
        return self._raw_message.get('ts')

    def is_type_message(self):
        return bool('message' == self.type)

    def is_bot_message(self):
        return bool('bot_message' == self.subtype or self._raw_message.get('bot_id'))

    def is_suppress_notification(self):
        return bool(self._raw_message.get('suppress_notification'))


class Response:

    def __init__(self, request: Message, text: str, method: str = 'chat.postMessage', **kwargs):
        """
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
        d = {'method': self.method, 'text': self.text, 'channel': self._request.channel}
        return d

    def to_dict(self) -> dict:
        data = self._base()
        data.update(self.kw)
        return data
