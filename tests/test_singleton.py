import typing as t

from software_patterns import Singleton


def test_singleton():
    class MySingleton(metaclass=Singleton):
        def __init__(self, data: t.Mapping):
            self.data = data

    instance_1 = MySingleton({'a': 1})
    instance_2 = MySingleton({'b': 2})

    assert id(instance_1) == id(instance_2)
    assert instance_1.data['a'] == instance_2.data['a'] == 1
    assert 'b' not in instance_1.data
    assert 'b' not in instance_2.data

    instance_1.data['c'] = 0

    assert instance_2.data['c'] == 0
