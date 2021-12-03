"""Implementation of the object pool"""
from typing import Dict, Generic, TypeVar, Any, Callable, Optional, Union
import types
from typing import Callable, Generic, Protocol, Any, Union, TypeVar, Dict


__all__ = ['ObjectsPool']



DictKey = Union[int, str]
T = TypeVar('T')


class ObjectsPool(Generic[T]):
    """Class of objects that are able to return a reference to an object upon request.

    Whenever an object is requested, it is checked whether it exists in the pool.
    Then if it exists, a reference is returned, otherwise a new object is
    constructed (given the provided callable) and its reference is returned.

    Arguments:
        constructor (callable): able to construct the object given arguments
        objects (dict): the data structure representing the object pool
    """
    constructor: Callable[..., T]
    _build_hash: Callable[..., DictKey]
    _objects: Dict[DictKey, T]

    def __new__(cls, callback: Callable[..., T], hash_callback: Optional[Callable[..., Union[int, str]]]=None):
        pool = super().__new__(cls)
        pool.constructor = callback
        def get_build_hash(hash_callback):
            def build_hash(self, *args, **kwargs):
                return hash_callback(*args, **kwargs)
            return build_hash

        pool._build_hash = hash_callback if callable(hash_callback) else types.MethodType(get_build_hash(cls.__build_hash), pool)
        pool._objects = {}
        return pool

    @staticmethod
    def __build_hash(*args: Any, **kwargs: Any) -> int:
        r"""Construct a hash out of the input \*args and \*\*kwargs."""
        return hash('-'.join([str(_) for _ in args] + [f'{key}={str(value)}' for key, value in kwargs.items()]))

    def get_object(self, *args: Any, **kwargs: Any) -> T:
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
