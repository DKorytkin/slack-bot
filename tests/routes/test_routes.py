from unittest.mock import MagicMock

import pytest

from slack_bot.routes import Route, Routers, RoutersTable


def test_routes_init():
    # Refresh singleton instance
    RoutersTable.instance = None

    routes = Routers()
    assert isinstance(routes.table, RoutersTable)


def test_routes_str():
    # Refresh singleton instance
    RoutersTable.instance = None

    routes = Routers()
    assert str(routes) == '<Routers has 0>'
    routes.table.add_route('path', lambda x: x)
    assert str(routes) == '<Routers has 1>'


def test_routes_length():
    # Refresh singleton instance
    RoutersTable.instance = None

    routes = Routers()
    assert len(routes) == 0
    routes.table.add_route('path', lambda x: x)
    assert len(routes) == 1


@pytest.mark.parametrize('params', (
    {'route': 'hello'},
    {'route': 'hello', 'channels': ['C1']},
    {'route': 'hello', 'channels': ['C1'], 'users': ['U1']}))
def test_find_exist_route(params):
    # Refresh singleton instance
    RoutersTable.instance = None
    table = RoutersTable()
    request = MagicMock(
        user_id='U1',
        channel='C1',
        text='hello',
        **{'is_bot_message.return_value': False}
    )

    @table.route('how do you do?')
    def answer(request):
        pass

    @table.route(**params)
    def hello(request):
        pass

    routes = Routers()
    route = routes.find_route(request)
    assert isinstance(route, Route)
    # TODO need fix after implement parse in route
    assert route.route == request.text
    assert route.handler == hello


@pytest.mark.parametrize('params', (
    {'route': 'hi!'},
    {'route': 'hello', 'channels': ['C2']},
    {'route': 'hello', 'users': ['U2']},
    {'route': 'hello', 'channels': ['C2'], 'users': ['U2']},
    {'route': 'hello', 'channels': ['C2'], 'users': ['U1']},
    {'route': 'hello', 'channels': ['C1'], 'users': ['U2']}))
def test_find_not_exist_route(params):
    # Refresh singleton instance
    RoutersTable.instance = None
    request = MagicMock(
        user_id='U1',
        channel='C1',
        text='hello',
        **{'is_bot_message.return_value': False}
    )
    table = RoutersTable()

    @table.route('how do you do?')
    def answer(request):
        pass

    @table.route(**params)
    def hello(request):
        pass

    routes = Routers()
    route = routes.find_route(request)
    assert route is None
