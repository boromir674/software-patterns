"""Implementation of the object pool"""
from typing import Dict, Generic, TypeVar, Any, Callable, Optional, Union
import types


__all__ = ['ObjectsPool']



DictKey = Union[int, str]
ObjectType = TypeVar('ObjectType')

RuntimeBuildHashCallable = Callable[..., Union[int, str]]


def adapt_build_hash(a_callable: RuntimeBuildHashCallable):
    def build_hash(_self: ObjectType, *args, **kwargs):
        return a_callable(*args, **kwargs)
    return build_hash


class ObjectsPool(Generic[ObjectType]):
    """Class of objects that are able to return a reference to an object upon request.

    Whenever an object is requested, it is checked whether it exists in the pool.
    Then if it exists, a reference is returned, otherwise a new object is
    constructed (given the provided callable) and its reference is returned.

    Arguments:
        constructor (callable): able to construct the object given arguments
        objects (dict): the data structure representing the object pool
    """
    _objects: Dict[DictKey, ObjectType]

    user_supplied_callaback: Dict[bool, Callable] = {
        True: lambda callback: callback,
        False: lambda callback: ObjectsPool.__build_hash,
    }

    def __init__(self, callback: Callable[..., ObjectType], hash_callback: Optional[RuntimeBuildHashCallable]=None):
        self.constructor = callback
        build_hash_callback = self.user_supplied_callaback[callable(hash_callback)](hash_callback)
        self._build_hash = types.MethodType(adapt_build_hash(build_hash_callback), self)
        self._objects = {}

    @staticmethod
    def __build_hash(*args: Any, **kwargs: Any) -> int:
        r"""Construct a hash out of the input \*args and \*\*kwargs."""
        return hash('-'.join([str(_) for _ in args] + [f'{key}={str(value)}' for key, value in kwargs.items()]))

    def get_object(self, *args: Any, **kwargs: Any) -> ObjectType:
        r"""Request an object from the pool.

        Get or create an object given the input parameters. Existence in the pool is done using the
        python-build-in hash function. The input \*args and \*\*kwargs serve as
        input in the hash function to create unique keys with which to "query" the object pool.

        Returns:
            object: the reference to the object that corresponds to the input
            arguments, regardless of whether it was found in the pool or not
        """
        key = self._build_hash(*args, **kwargs)
        if key not in self._objects:
            self._objects[key] = self.constructor(*args, **kwargs)
        return self._objects[key]
