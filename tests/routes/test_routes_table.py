from slack_bot.routes import RoutersTable, Route


def test_make_single_table():
    # Refresh singleton instance
    RoutersTable.instance = None

    t1 = RoutersTable()
    t2 = RoutersTable()
    assert t1 == t2
    assert t1 is t2
    t1.add_route('path1', lambda x: x)
    t2.add_route('path2', lambda x: x)
    assert len(t1.routes) == 2
    assert t1.routes == t2.routes


def test_routers_table_init():
    # Refresh singleton instance
    RoutersTable.instance = None

    t = RoutersTable()
    assert isinstance(t.routes, set)
    assert t.routes == set()


def test_routers_table_length():
    # Refresh singleton instance
    RoutersTable.instance = None

    table = RoutersTable()
    assert len(table) == 0
    table.add_route('some path', lambda x: x)
    assert len(table) == 1


def test_routers_table_str():
    # Refresh singleton instance
    RoutersTable.instance = None

    table = RoutersTable()
    assert str(table) == '<RoutersTable has 0 routes>'
    table.add_route('some path', lambda x: x)
    assert str(table) == '<RoutersTable has 1 routes>'


def test_add_route_full_fields():
    # Refresh singleton instance
    RoutersTable.instance = None

    t = RoutersTable()
    t.add_route('path', lambda x: x, channels=['C1'], users=['U1'])
    assert len(t.routes) == 1
    assert all([isinstance(r, Route) for r in t.routes])


def test_add_route_short_fields():
    # Refresh singleton instance
    RoutersTable.instance = None

    t = RoutersTable()
    t.add_route('path', lambda x: x)
    assert len(t.routes) == 1
    assert all([isinstance(r, Route) for r in t.routes])


def test_add_many_routes():
    # Refresh singleton instance
    RoutersTable.instance = None

    t = RoutersTable()
    for i in range(3):
        t.add_route(f'path_{i}', lambda x: x)
    assert len(t.routes) == 3
    assert all([isinstance(r, Route) for r in t.routes])


def test_add_routes():
    # Refresh singleton instance
    RoutersTable.instance = None

    my_routes = [
        Route('path1', lambda x: x),
        Route('path2', lambda x: x, channels=['C1'], users=['U1'])
    ]
    t = RoutersTable()
    t.add_routes(my_routes)
    assert len(t.routes) == 2
    assert all([isinstance(r, Route) for r in t.routes])
    assert t.routes == set(my_routes)


def test_route_decorator():
    # Refresh singleton instance
    RoutersTable.instance = None

    table = RoutersTable()

    @table.route('path')
    def my_action(request):
        pass

    assert isinstance(table.routes, set)
    assert len(table.routes) == 1
    assert all([isinstance(r, Route) for r in table.routes])


def test_route_decorator_with_full_attributes():
    # Refresh singleton instance
    RoutersTable.instance = None

    table = RoutersTable()

    @table.route('path1', channels=['C1'], users=['U1'])
    def my_action1(request):
        pass

    @table.route('path2', channels=['C2'], users=['U2'])
    def my_action1(request):
        pass

    assert isinstance(table.routes, set)
    assert len(table.routes) == 2
    assert all([isinstance(r, Route) for r in table.routes])
