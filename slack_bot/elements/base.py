import abc
import json


class Base(metaclass=abc.ABCMeta):

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        return json.dumps(self.to_dict())

    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError


class Block:
    """
    {
        "blocks": []
    }
    """
