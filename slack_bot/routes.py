

class Singleton(type):

    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class Route:

    def __init__(self, rout, handler, channels=None, users=None):
        self.rout = rout
        self.handler = handler
        self.channels = channels
        self.users = users

    def __str__(self):
        return f'<Rout {self.rout} {self.handler}>'

    def __repr__(self):
        return self.__str__()

    def check(self, message) -> bool:
        # TODO need implementation regexp
        # from parse import parse???
        # TODO need validate if have channels or users
        return bool(self.rout == message)


class RoutersTable(metaclass=Singleton):

    def __init__(self):
        self.routes = set()

    def __call__(self, rout, handler, channels=None, users=None):
        self.add_route(rout, handler, channels, users)

    def route(self, rout, channels=None, users=None):
        """
        decorator
        """
        def wrapper(handler):
            self.add_route(rout, handler, channels, users)
            return handler
        return wrapper

    def add_route(self, rout, handler, channels=None, users=None):
        """
        :param str rout: message
        :param function handler: action for message
        :param list channels: subscribe by channels only
        :param list users: subscribe by user messages only
        """
        self.routes.add(Route(rout, handler, channels, users))

    def add_routes(self, routes: list):
        self.routes.update(set(routes))


class Routers:

    def __init__(self):
        self.table = RoutersTable()

    def find_handler(self, msg):
        for rout in self.table.routes:
            if rout.check(msg):
                return rout.handler
        return None
