from unittest.mock import MagicMock

import pytest

from slack_bot.routes import Route, Routers, RoutersTable


MOCK_REQUEST = MagicMock(user='U1', channel='C1', text='hello')


def test_routes_init():
    # Refresh singleton instance
    RoutersTable.instance = None

    routes = Routers()
    assert isinstance(routes.table, RoutersTable)


@pytest.mark.parametrize('params', (
    {'route': 'hello'},
    {'route': 'hello', 'channels': ['C1']},
    {'route': 'hello', 'channels': ['C1'], 'users': ['U1']}))
def test_find_exist_route(params):
    """
    MOCK_REQUEST = MagicMock(user='U1', channel='C1', text='hello')
    """
    # Refresh singleton instance
    RoutersTable.instance = None
    table = RoutersTable()

    @table.route('how do you do?')
    def answer(request):
        pass

    @table.route(**params)
    def hello(request):
        pass

    routes = Routers()
    route = routes.find_route(MOCK_REQUEST)
    assert isinstance(route, Route)
    # TODO need fix after implement parse in route
    assert route.route == MOCK_REQUEST.text
    assert route.handler == hello


@pytest.mark.parametrize('params', (
    {'route': 'hi!'},
    {'route': 'hello', 'channels': ['C2']},
    {'route': 'hello', 'users': ['U2']},
    {'route': 'hello', 'channels': ['C2'], 'users': ['U2']},
    {'route': 'hello', 'channels': ['C2'], 'users': ['U1']},
    {'route': 'hello', 'channels': ['C1'], 'users': ['U2']}))
def test_find_not_exist_route(params):
    """
    MOCK_REQUEST = MagicMock(user='U1', channel='C1', text='hello')
    """
    # Refresh singleton instance
    RoutersTable.instance = None
    table = RoutersTable()

    @table.route('how do you do?')
    def answer(request):
        pass

    @table.route(**params)
    def hello(request):
        pass

    routes = Routers()
    route = routes.find_route(MOCK_REQUEST)
    assert route is None
