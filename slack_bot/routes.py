from typing import Callable, List, Set, Union

from slack_bot.models import Message


class Singleton(type):

    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class Route:

    def __init__(self, route, handler, channels=None, users=None):
        self.route = route
        self.handler = handler
        self.channels = channels
        self.users = users

    def __str__(self):
        return (
            f'<Route {repr(self.route)} handler={self.handler} '
            f'channels={self.channels} users={self.users}>'
        )

    def __repr__(self):
        return self.__str__()

    def validate_users(self, user: str) -> bool:
        if not self.users:
            return True
        return bool(user in self.users)

    def validate_channels(self, channel: str) -> bool:
        if not self.channels:
            return True
        return bool(channel in self.channels)

    def validate_message(self, message: str) -> bool:
        # TODO need implementation regexp
        # from parse import parse???
        return bool(self.route == message)

    def validated(self, request: Message) -> bool:
        if not self.validate_users(request.user):
            return False

        if not self.validate_channels(request.channel):
            return False

        if not self.validate_message(request.text):
            return False

        # message.match_info = info
        return True


class RoutersTable(metaclass=Singleton):

    def __init__(self):
        self.routes = set()

    def route(self, rout: str, channels: List[str] = None, users: List[str] = None) -> Callable:
        """
        Decorator add some bot actions if route wen equal message
        Usage:
            table = RoutersTable()

            @table.route('hello')
            def some_bot_action(request):
                return Response(request=request, text='Hi!')

        :param str rout: target message in slack
        :param list[str] channels: only for subscribe channels
        :param list[str] users: only for subscribe users
        """
        def wrapper(handler):
            self.add_route(rout, handler, channels, users)
            return handler
        return wrapper

    def add_route(
        self,
        rout: str,
        handler: Callable,
        channels: List[str] = None,
        users: List[str] = None
    ) -> Set[Route]:
        """
        :param str rout: message
        :param function handler: action for message
        :param list channels: subscribe by channels only
        :param list users: subscribe by user messages only
        """
        self.routes.add(Route(rout, handler, channels, users))
        return self.routes

    def add_routes(self, routes: list) -> Set[Route]:
        """
        Add handlers for all bot actions
        Usage:
            table = RoutersTable()
            table.add_routes([
                Route('hello', say_hello_handler),
                Route('how do you do?', answer_handler),
            ])

        :param list[Route] routes:
        :return: list[Route]
        """
        self.routes.update(set(routes))
        return self.routes


class Routers:

    def __init__(self):
        self.table = RoutersTable()

    def find_route(self, msg: Message) -> Union[Route, None]:
        for rout in self.table.routes:
            if rout.validated(msg):
                return rout
        return None
