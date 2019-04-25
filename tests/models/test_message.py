import pytest

from slack_bot.models import Message


@pytest.mark.parametrize('raw', (
    [{"type": "user_typing", "channel": "C0DEW8K45", "user": "U0DF0B546"}],
    {"type": "user_typing", "channel": "C0DEW8K45", "user": "U0DF0B546"}))
def test_message_init(raw):
    m = Message(raw)
    assert isinstance(m._raw, type(raw))
    assert isinstance(m._raw_message, dict)
    assert m._raw_message
    assert m._match_info == {}


def test_message_str_with_info():
    m = Message([{"type": "user_typing", "channel": "C0DEW8K45", "user": "U0DF0B546"}])
    assert str(m) == '<Message user_typing user=U0DF0B546 channel=C0DEW8K45 info={}>'


def test_message_str_without_info():
    m = Message([{"type": "user_typing", "channel": "C0DEW8K45", "user": "U0DF0B546"}])
    m.match_info = {'name': 'bot'}
    assert str(m) == "<Message user_typing user=U0DF0B546 channel=C0DEW8K45 info={'name': 'bot'}>"


def test_message_match_info():
    m = Message([{"type": "user_typing", "channel": "C0DEW8K45", "user": "U0DF0B546"}])
    assert m._match_info == {}
    assert m.match_info == {}
    m.match_info = {'name': 'bot'}
    assert m._match_info == {'name': 'bot'}
    assert m.match_info == {'name': 'bot'}


@pytest.mark.parametrize('raw, exp_result', (
    ([{"type": "message"}], True),
    ([{"type": "message", "channel": "C0DEW8K45", "user": "U0DF0B546"}], True),
    ([{}], False),
    ([{"type": "msg", "channel": "C0DEW8K45", "user": "U0DF0B546"}], False),
    ([{"type": "user_typing", "channel": "C0DEW8K45", "user": "U0DF0B546"}], False)))
def test_message_is_type_message(raw, exp_result):
    m = Message(raw)
    assert m.is_type_message() is exp_result


@pytest.mark.parametrize('raw, exp_result', (
    ([{"suppress_notification": False}], False),
    ([{"suppress_notification": True}], True),
    ([{
        "client_msg_id": "eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a",
        "suppress_notification": False,
        "type": "message",
        "text": "as",
        "user": "U0DF0B546",
        "team": "T0DF1FYHE",
        "channel": "C0DEW8K45",
        "event_ts": "1555937221.001500",
        "ts": "1555937221.001500"
    }], False),
    ([{
        "client_msg_id": "eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a",
        "suppress_notification": True,
        "type": "message",
        "text": "as",
        "user": "U0DF0B546",
        "team": "T0DF1FYHE",
        "channel": "C0DEW8K45",
        "event_ts": "1555937221.001500",
        "ts": "1555937221.001500"
    }], True)))
def test_message_is_suppress_notification(raw, exp_result):
    m = Message(raw)
    assert m.is_suppress_notification() is exp_result


@pytest.mark.parametrize('raw, exp_result', (
    ([{"subtype": "message_changed"}], False),
    ([{"subtype": "bot_message"}], True),
    ([{"subtype": "message_changed", "bot_id": "BHVN4M5A5"}], True),
    ([{
        "client_msg_id": "eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a",
        "suppress_notification": False,
        "type": "message",
        "subtype": "bot_message",
        "text": "as",
        "user": "U0DF0B546",
        "team": "T0DF1FYHE",
        "channel": "C0DEW8K45",
        "event_ts": "1555937221.001500",
        "ts": "1555937221.001500"
    }], True),
    ([{
        "client_msg_id": "eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a",
        "suppress_notification": True,
        "type": "message",
        "text": "as",
        "bot_id": "BHVN4M5A5",
        "user": "U0DF0B546",
        "team": "T0DF1FYHE",
        "channel": "C0DEW8K45",
        "event_ts": "1555937221.001500",
        "ts": "1555937221.001500"
    }], True)))
def test_message_is_bot_message(raw, exp_result):
    m = Message(raw)
    assert m.is_bot_message() is exp_result


def test_base_message_attributes():
    m = Message([{
        "client_msg_id": "eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a",
        "suppress_notification": False,
        "type": "message",
        "text": "as",
        "user": "U0DF0B546",
        "team": "T0DF1FYHE",
        "channel": "C0DEW8K45",
        "event_ts": "1555937221.001500",
        "ts": "1555937221.001500"
    }])
    assert m.user_id == 'U0DF0B546'
    assert m.user == '<@U0DF0B546>'
    assert m.type == 'message'
    assert m.subtype is None
    assert m.client_msg_id == 'eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a'
    assert m.team == 'T0DF1FYHE'
    assert m.channel == 'C0DEW8K45'
    assert m.event_ts == '1555937221.001500'
    assert m.ts == '1555937221.001500'


def test_edited_message_attributes():
    m = Message([{
        "type": "message",
        "subtype": "message_changed",
        "hidden": True,
        "message": {
            "client_msg_id": "eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a",
            "type": "message",
            "text": "ass",
            "user": "U0DF0B546",
            "edited": {
                "user": "U0DF0B546",
                "ts": "1555937291.000000"
            },
            "ts": "1555937221.001500"
        },
        "channel": "C0DEW8K45",
        "previous_message": {
            "client_msg_id": "eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a",
            "type": "message",
            "text": "as",
            "user": "U0DF0B546",
            "ts": "1555937221.001500"
        },
        "event_ts": "1555937291.001600",
        "ts": "1555937291.001600"
    }])
    assert m.user_id == 'U0DF0B546'
    assert m.user == '<@U0DF0B546>'
    assert m.type == 'message'
    assert m.subtype == 'message_changed'
    assert m.client_msg_id == 'eb4cbc49-e1a8-4c47-b501-0ac0dbbc2c4a'
    assert m.team is None
    assert m.channel == 'C0DEW8K45'
    assert m.event_ts == '1555937291.001600'
    assert m.ts == '1555937291.001600'


def test_hello_action_message_attributes():
    m = Message([{
        "type": "user_typing",
        "channel": "C0DEW8K45",
        "user": "U0DF0B546"
    }])
    assert m.user_id == 'U0DF0B546'
    assert m.user == '<@U0DF0B546>'
    assert m.type == 'user_typing'
    assert m.channel == 'C0DEW8K45'
    assert m.subtype is None
    assert m.client_msg_id is None
    assert m.team is None
    assert m.event_ts is None
    assert m.ts is None
