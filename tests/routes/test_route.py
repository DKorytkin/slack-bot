from unittest.mock import MagicMock

import pytest

from slack_bot.routes import Route


MOCK_REQUEST = MagicMock(user='U1', channel='C1', text='hello')


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
    assert r.validate_users(user) is exp_result


@pytest.mark.parametrize('subscribers', (None, [], set(), tuple()))
@pytest.mark.parametrize('user, exp_result', (
    ('U1', True),
    ('U', True),
    (123, True),
    (True, True),
    ('U2', True)))
def test_validate_users_without_subscribers(user, exp_result, subscribers):
    r = Route('path', my_handler, ['#general'], subscribers)
    assert r.validate_users(user) is exp_result


@pytest.mark.parametrize('channel, exp_result', (
    ('#general', True),
    ('#', False),
    ('general', False),
    (123, False),
    (True, False),
    ('C2', False)))
def test_validate_channels_with_subscribers(channel, exp_result):
    r = Route('path', my_handler, ['#general'])
    assert r.validate_channels(channel) is exp_result


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
    assert r.validate_channels(channel) is exp_result


@pytest.mark.parametrize('route, msg, exp_result', (
    ('', '', True),
    ('', 'fail', False),
    ('', True, False),
    (None, True, False),
    (None, None, True),
    ('my message', 'my message', True)))
def test_validate_message(route, msg, exp_result):
    r = Route(route, my_handler)
    assert r.validate_message(msg) is exp_result


@pytest.mark.parametrize('route, channels, users, exp_result', (
    ('hello', [], [], True),
    ('hello', ['C1'], [], True),
    ('hello', ['C1'], ['U1'], True),
    ('hell', [], [], False),
    ('hell', ['C1'], [], False),
    ('hell', ['C1'], ['U1'], False),
    ('hello', ['C2'], [], False),
    ('hello', [], ['U2'], False),
    ('hello', ['C1'], ['U2'], False),))
def test_validated(route, channels, users, exp_result):
    """
    MOCK_REQUEST = MagicMock(user='U1', channel='C1', text='hello')
    """
    r = Route(route=route, handler=my_handler, channels=channels, users=users)
    assert r.validated(MOCK_REQUEST) is exp_result
