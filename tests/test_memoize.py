import pytest


@pytest.fixture
def simple_memoize():
    from software_patterns import ObjectsPool

    class TestClass:
        def __init__(self, number, name):
            self.number = number
            self.name = name

        @staticmethod
        def factory_method(arg1, arg2, **kwargs):
            return TestClass(arg1, arg2)
    return ObjectsPool(TestClass.factory_method)


def test_simple_memoize(simple_memoize):
    runtime_args = (7, 'gg')
    runtime_kwargs = dict(kwarg1='something', kwarg2=[1, 2])
    instance1 = simple_memoize.get_object(*runtime_args, **runtime_kwargs)
    instance2 = simple_memoize.get_object(*runtime_args, **runtime_kwargs)
    assert instance1 == instance2
    assert id(instance1) == id(instance2)
    hash1 = simple_memoize._build_hash(*runtime_args, **runtime_kwargs)
    assert hash1 == hash('-'.join([str(_) for _ in runtime_args] + [f'{key}={str(value)}' for key, value in runtime_kwargs.items()]))
