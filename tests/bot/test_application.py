from unittest.mock import MagicMock, patch

import pytest

from slack_bot.bot import Application
from slack_bot.models import Response
from slack_bot.routes import Routers, Route, RoutersTable


TOKEN = 'SUPER_SECRET_SLACK_TOKEN'


def test_app_init():
    app = Application(TOKEN)
    assert app._token == TOKEN
    assert app._client is None
    assert app._bot_id is None
    assert isinstance(app._routers, Routers)
    assert len(app._routers) == 0


def test_app_bot_id():
    app = Application(TOKEN)
    mock_client = MagicMock(**{'api_call.return_value': {'user_id': 'UBOT1'}})
    app.client = mock_client
    assert app.bot_id == 'UBOT1'
    mock_client.api_call.assert_called_once_with('auth.test')


def test_app_get_client():
    app = Application(TOKEN)
    mock_client = MagicMock()
    with patch('slack_bot.bot.Application._client_connected', return_value=mock_client) as mock:
        assert app.client == mock_client
        assert app._client == mock_client
        mock.assert_called_once()
    new_client = MagicMock()
    app.client = new_client
    assert app._client == new_client
    assert app.client == new_client


def test_app_set_client():
    app = Application(TOKEN)
    new_client = MagicMock()
    app.client = new_client
    assert app._client == new_client
    assert app.client == new_client


def test_app__client_connected():
    app = Application(TOKEN)
    with pytest.raises(Exception):
        app._client_connected()


def test_app_send():
    app = Application(TOKEN)
    mock_client = MagicMock(**{'api_call.return_value': {'user_id': 'UBOT1'}})
    app.client = mock_client
    response = Response(MagicMock(user='U0DF0B546', channel='C0DEW8K45', text='hi!'), text='OK')
    assert app._send(response) is True
    mock_client.api_call.assert_called_once_with(
        as_user=True,
        channel='C0DEW8K45',
        icon_emoji=':ghost:',
        method='chat.postMessage',
        text='OK'
    )


def test_app_route():
    # Refresh singleton instance
    RoutersTable.instance = None

    app = Application(TOKEN)

    @app.route('deploy {app:w}')
    def deploy(request):
        current_app = request.match_info['app']
        return Response(request, text=f'Start deploy {current_app}')

    assert len(app._routers) == 1
    route = list(app._routers.table.routes)[0]
    assert isinstance(route, Route)
    assert route.handler == deploy


def test_app_add_routes():
    # Refresh singleton instance
    RoutersTable.instance = None

    app = Application(TOKEN)

    def say_hello(request):
        return Response(request, text='Hi!')

    def do_deploy(request):
        current_app = request.match_info['app']
        return Response(request, text=f'Start deploy {current_app}')

    app.add_routes([
        Route('deploy {app:w}', do_deploy),
        Route('hello', say_hello),
    ])
    assert len(app._routers) == 2
    route1 = list(app._routers.table.routes)[0]
    route2 = list(app._routers.table.routes)[1]
    assert all([isinstance(r, Route) for r in app._routers.table.routes])
    assert route1.handler == do_deploy
    assert route2.handler == say_hello


def test_app_process_message():
    pass
