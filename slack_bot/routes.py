from typing import Callable, List, Set, Union

from parse import search

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

    def validate_users(self, request: Message) -> bool:
        if not request.user or request.is_bot_message():
            return False

        if not self.users:
            return True
        return bool(request.user in self.users)

    def validate_channels(self, request: Message) -> bool:
        if not request.channel:
            return False

        if not self.channels:
            return True
        return bool(request.channel in self.channels)

    def validate_message(self, request: Message) -> bool:
        if not request.text or not isinstance(request.text, str):
            return False

        result = search(self.route, request.text)
        if not result:
            return False

        request.match_info = result.named
        request.info = result.fixed
        return True

    def validated(self, request: Message) -> bool:
        if not self.validate_users(request):
            return False

        if not self.validate_channels(request):
            return False

        if not self.validate_message(request):
            return False

        return True


class RoutersTable(metaclass=Singleton):

    def __init__(self):
        self.routes = set()

    def __len__(self):
        return len(self.routes)

    def __str__(self):
        return f'<RoutersTable has {self.__len__()} routes>'

    def __repr__(self):
        return self.__str__()

    def route(self, route: str, channels: List[str] = None, users: List[str] = None) -> Callable:
        """
        Decorator add some bot actions if route wen equal message
        Usage:
            table = RoutersTable()

            @table.route('hello')
            def some_bot_action(request):
                return Response(request=request, text='Hi!')

        :param str route: target message in slack
        :param list[str] channels: only for subscribe channels
        :param list[str] users: only for subscribe users
        """
        def wrapper(handler):
            self.add_route(route, handler, channels, users)
            return handler
        return wrapper

    def add_route(
        self,
        route: str,
        handler: Callable,
        channels: List[str] = None,
        users: List[str] = None
    ) -> Set[Route]:
        """
        :param str route: message
        :param function handler: action for message
        :param list channels: subscribe by channels only
        :param list users: subscribe by user messages only
        """
        self.routes.add(Route(route, handler, channels, users))
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

    def __len__(self):
        return len(self.table)

    def __str__(self):
        return f'<Routers has {self.__len__()}>'

    def __repr__(self):
        return self.__str__()

    def find_route(self, msg: Message) -> Union[Route, None]:
        for route in self.table.routes:
            if route.validated(msg):
                return route
        return None
