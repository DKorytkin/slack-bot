
from slack_bot.routes import Singleton


def test_singleton_classes():
    class MyClass(metaclass=Singleton):
        def __init__(self, data):
            self.data = data

    instance1 = MyClass(1)
    instance2 = MyClass(2)
    assert instance1 is instance2
    assert instance1 == instance2
    assert instance1.data == 1
    assert instance1.data == instance2.data
