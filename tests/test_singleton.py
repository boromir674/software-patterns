import typing as t

import pytest

from software_patterns import Singleton


def test_singleton(assert_same_objects):
    class MySingleton(metaclass=Singleton):
        def __init__(self, data: t.MutableMapping):
            self.data = data

    instance_1 = MySingleton({'a': 1})
    instance_2 = MySingleton({'b': 2})

    assert_same_objects(instance_1, instance_2)

    assert instance_1.data['a'] == instance_2.data['a'] == 1
    assert 'b' not in instance_1.data
    assert 'b' not in instance_2.data

    instance_1.data['c'] = 0

    assert instance_2.data['c'] == 0


@pytest.fixture
def assert_same_objects():
    def _assert_same_objects(obj1, obj2):
        assert id(obj1) == id(obj2)
        attributes_1 = list(dir(obj1))
        attributes_2 = list(dir(obj2))
        assert attributes_1 == attributes_2
        for attr_name in set(attributes_1).difference(
            {
                '__delattr__',
                '__init__',
                '__gt__',
                '__ne__',
                '__dir__',
                '__repr__',
                '__setattr__',
                '__le__',
                '__subclasshook__',
                '__str__',
                '__format__',
                '__lt__',
                '__eq__',
                '__reduce_ex__',
                '__getattribute__',
                '__reduce__',
                '__init_subclass__',
                '__hash__',
                '__sizeof__',
                '__ge__',
                '__getstate__',
            }
        ):
            print(attr_name)
            assert getattr(obj1, attr_name) == getattr(obj2, attr_name)
            assert id(getattr(obj1, attr_name)) == id(getattr(obj2, attr_name))

    return _assert_same_objects
