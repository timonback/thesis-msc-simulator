import inspect
import json
from collections import namedtuple
from decimal import Decimal
from types import SimpleNamespace


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif isinstance(obj, Decimal):
            return "%f" % obj
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return obj
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        # unable to handle. Let base class raise the exception
        return super().default(obj)

    @staticmethod
    def dict_to_object_recursive(d: dict):
        obj = SimpleNamespace(**d)
        for ele in obj.__dict__:
            if isinstance(obj.__dict__[ele], dict):
                obj.__dict__[ele] = JsonEncoder.dict_to_object(obj.__dict__[ele])
        return obj

    @staticmethod
    def dict_to_object(d: dict):
        obj = namedtuple('X', d.keys())(*d.values())
        return obj

    def to_obj(self, json_data):
        return json.loads(json_data, object_hook=JsonEncoder.dict_to_object)
