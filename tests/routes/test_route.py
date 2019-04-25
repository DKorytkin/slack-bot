from unittest.mock import MagicMock

import pytest

from slack_bot.routes import Route


def my_handler(request):
    pass


def test_route_str():
    r = Route('path', my_handler, ['#general'], ['U1'])
    assert str(r) == f"<Route 'path' handler={my_handler} channels=['#general'] users=['U1']>"


def test_init_with_full_attributes():
    r = Route('path', my_handler, ['#general'], ['U1'])
    assert r.route == 'path'
    assert r.handler == my_handler
    assert r.channels == ['#general']
    assert r.users == ['U1']


def test_init_with_short_attributes():
    r = Route('path', my_handler)
    assert r.route == 'path'
    assert r.handler == my_handler
    assert r.channels is None
    assert r.users is None


@pytest.mark.parametrize('params', (
    {},
    {'route': 'path'},
    {'route': 'path', 'channels': ['#general'], 'users': ['U1']},
    {'handler': my_handler},
    {'handler': my_handler, 'channels': ['#general'], 'users': ['U1']},))
def test_init_require_attributes(params):
    with pytest.raises(TypeError):
        Route(**params)


@pytest.mark.parametrize('user, exp_result', (
    ('U1', True),
    ('U', False),
    (123, False),
    (True, False),
    ('U2', False)))
def test_validate_users_with_subscribers(user, exp_result):
    r = Route('path', my_handler, ['#general'], ['U1'])
    request = MagicMock(user_id=user, **{'is_bot_message.return_value': False})
    assert r.validate_users(request) is exp_result


@pytest.mark.parametrize('subscribers', (None, [], set(), tuple()))
@pytest.mark.parametrize('user, exp_result', (
    ('U1', True),
    ('U', True),
    (123, True),
    (True, True),
    ('U2', True)))
def test_validate_users_without_subscribers(user, exp_result, subscribers):
    r = Route('path', my_handler, ['#general'], subscribers)
    request = MagicMock(user_id=user, **{'is_bot_message.return_value': False})
    assert r.validate_users(request) is exp_result


def test_validate_users_bot_without_subscribers():
    r = Route('path', my_handler, ['#general'])
    request = MagicMock(user_id='U1', **{'is_bot_message.return_value': True})
    assert r.validate_users(request) is False


def test_validate_users_bot_with_subscribers():
    r = Route('path', my_handler, ['#general'], users=['U1'])
    request = MagicMock(user_id='U1', **{'is_bot_message.return_value': True})
    assert r.validate_users(request) is False


@pytest.mark.parametrize('channel, exp_result', (
    ('#general', True),
    ('#', False),
    ('general', False),
    (123, False),
    (True, False),
    ('C2', False)))
def test_validate_channels_with_subscribers(channel, exp_result):
    r = Route('path', my_handler, ['#general'])
    assert r.validate_channels(MagicMock(channel=channel)) is exp_result


@pytest.mark.parametrize('subscribers', (None, [], set(), tuple()))
@pytest.mark.parametrize('channel, exp_result', (
    ('#general', True),
    ('#', True),
    ('general', True),
    (123, True),
    (True, True),
    ('C2', True)))
def test_validate_channels_without_subscribers(channel, exp_result, subscribers):
    r = Route('path', my_handler, subscribers)
    assert r.validate_channels(MagicMock(channel=channel)) is exp_result


@pytest.mark.parametrize('route, msg, exp_result', (
    ('', '', False),
    ('', True, False),
    (None, True, False),
    (None, None, False),
    ('deploy {app:l}', 'deploy 123', False),
    ('deploy {app:^w} to v{version:^S}', 'deploy rc', False),
    ('deploy {app:^w} to v{version:^S}', 'deploy rc to v', False),
    ('<@{user:w}> {ask:^w}', 'hi <@UHVN4M5B3>!', False),
    ('deploy {:l}', 'deploy 12', False)))
def test_validate_not_correct_message(route, msg, exp_result):
    r = Route(route, my_handler)
    request = MagicMock(user_id='U1', channel='C1', text=msg, match_info={}, info=None)
    assert r.validate_message(request) is exp_result
    assert request.match_info == {}
    assert request.info is None


@pytest.mark.parametrize('route, msg, exp_result, info, match', (
    ('', 'test', True, (), {}),
    ('deploy {:w}', 'deploy rc', True, ('rc',), {}),
    ('deploy {app:w}', 'deploy rc', True, (), {'app': 'rc'}),
    ('deploy {app:^w}', 'deploy   dev   ', True, (), {'app': 'dev'}),
    ('deploy {app:^w} to v{version:^d}', 'deploy rc to v2', True, (), {'app': 'rc', 'version': 2}),
    ('deploy {app:^w} to v{ver:^S}', 'deploy rc to v2.1 ', True, (), {'app': 'rc', 'ver': '2.1'}),
    ('<@{user:w}> {ask:^w}', '<@UHVN4M5B3> hi all!', True, (), {'ask': 'hi', 'user': 'UHVN4M5B3'}),
    ('my message', 'my message', True, (), {})))
def test_validate_correct_message(route, msg, exp_result, info, match):
    route = Route(route, my_handler)
    request = MagicMock(user_id='U1', channel='C1', text=msg, match_info={}, info=None)
    assert route.validate_message(request) is exp_result
    assert request.match_info == match
    assert request.info == info


@pytest.mark.parametrize('route, channels, users, exp_result', (
    ('hello', [], [], True),
    ('hello', ['C1'], [], True),
    ('hello', ['C1'], ['U1'], True),
    ('hell', [], [], True),
    ('hell', ['C1'], [], True),
    ('hell', ['C1'], ['U1'], True),
    ('hello', ['C2'], [], False),
    ('hello', [], ['U2'], False),
    ('hello', ['C1'], ['U2'], False),))
def test_validated(route, channels, users, exp_result):
    request = MagicMock(
        user_id='U1',
        channel='C1',
        text='hello',
        **{'is_bot_message.return_value': False}
    )
    r = Route(route=route, handler=my_handler, channels=channels, users=users)
    assert r.validated(request) is exp_result
