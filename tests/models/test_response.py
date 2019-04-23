from unittest.mock import MagicMock

from slack_bot.models import Response


MOCK_REQUEST = MagicMock(user='U0DF0B546', channel='C0DEW8K45', text='hi!')


def test_response_init_with_required_fields():
    resp = Response(MOCK_REQUEST, 'Hello someone!')
    assert resp._request == MOCK_REQUEST
    assert resp.text == 'Hello someone!'
    assert resp.method == 'chat.postMessage'
    assert isinstance(resp.kw, dict)
    assert not resp.kw


def test_response_init_with_optional_fields():
    resp = Response(
        request=MOCK_REQUEST,
        text='Hello someone!',
        method='auth.test',
        username='MyBotName',
        as_user=True
    )
    assert resp._request == MOCK_REQUEST
    assert resp.text == 'Hello someone!'
    assert resp.method == 'auth.test'
    assert isinstance(resp.kw, dict)
    assert resp.kw == {'username': 'MyBotName', 'as_user': True}


def test_base_response():
    exp_result = {
        'method': 'auth.test',
        'text': 'Hello someone!',
        'channel': MOCK_REQUEST.channel,
        'as_user': True,
        'icon_emoji': ':ghost:'
    }

    response = Response(
        request=MOCK_REQUEST,
        text='Hello someone!',
        method='auth.test',
        username='MyBotName',
        as_user=False
    )
    result = response._base()
    assert isinstance(result, dict)
    assert result == exp_result


def test_response_to_dict():
    exp_result = {
        'method': 'auth.test',
        'text': 'Hello someone!',
        'channel': MOCK_REQUEST.channel,
        'as_user': False,
        'icon_emoji': ':wink:',
        'mrkdwn': False,
        'username': 'MyBotName',
    }

    response = Response(
        request=MOCK_REQUEST,
        text='Hello someone!',
        method='auth.test',
        username='MyBotName',
        icon_emoji=':wink:',
        as_user=False,
        mrkdwn=False
    )
    result = response.to_dict()
    assert isinstance(result, dict)
    assert result == exp_result
