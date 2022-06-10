"""Implementation of the Memoize Software Design Pattern.

Memoize is implemented using an Object Pool which is queried by a key which is
the result of computing a hash given runtime arguments.

"""
import types
from typing import Any, Callable, Dict, Generic, Optional, TypeVar, Union

__all__ = ['ObjectsPool']


DictKey = Union[int, str]
ObjectType = TypeVar('ObjectType')

RuntimeBuildHashCallable = Callable[..., Union[int, str]]


def adapt_build_hash(a_callable: RuntimeBuildHashCallable):
    def build_hash(_self: ObjectType, *args, **kwargs):
        return a_callable(*args, **kwargs)

    return build_hash


class ObjectsPool(Generic[ObjectType]):
    """Cache objects and allow to query (the pool) using runtime arguments.

    Instances of the ObjectsPool class implement the Object Pool Software Design
    Creational Pattern.

    Whenever an object is requested, it is checked whether it exists in the
    pool by using the runtimetime arguments to query a python dictionary.
    If it exists, a reference is returned, otherwise a new object is
    constructed (given the provided callback) and its reference is returned.

    Example:
        >>> from software_patterns import ObjectsPool
        >>> class ClientClass:
        ...  def __init__(self, a: int, b: int):
        ...   pass

        >>> object_pool = ObjectsPool[ClientClass](ClientClass)

        >>> obj1 = object_pool.get_object(1, 2)
        >>> obj2 = object_pool.get_object(1, 3)
        >>> obj3 = object_pool.get_object(1, 2)

        >>> id(obj1) == id(obj3)
        True

        >>> len(object_pool._objects)
        2

    Args:
        callback (Callable[..., ObjectType]): constructs objects given arguments
        hash_callback (Optional[RuntimeBuildHashCallable], optional): option to
            overide the default hash key computer. Defaults to None.
    Returns:
        [type]: [description]
    """

    _objects: Dict[DictKey, ObjectType]

    user_supplied_callback: Dict[bool, Callable] = {
        True: lambda callback: callback,
        False: lambda callback: ObjectsPool.__build_hash,
    }

    def __init__(
        self,
        callback: Callable[..., ObjectType],
        hash_callback: Optional[RuntimeBuildHashCallable] = None,
    ):
        self.constructor = callback
        build_hash_callback = self.user_supplied_callback[callable(hash_callback)](
            hash_callback
        )
        self._build_hash = types.MethodType(adapt_build_hash(build_hash_callback), self)
        self._objects = {}

    @staticmethod
    def __build_hash(*args: Any, **kwargs: Any) -> int:
        r"""Construct a hash out of the input \*args and \*\*kwargs."""
        return hash(
            '-'.join(
                [str(_) for _ in args]
                + [f'{key}={str(value)}' for key, value in kwargs.items()]
            )
        )

    def get_object(self, *args: Any, **kwargs: Any) -> ObjectType:
        r"""Request an object from the pool.

        Get or create an object given the input arguments, which are used to
        create a unique hash key. The key is used to query a python dictionary
        and determine whether the object request refers to a cached object.

        Returns:
            object (ObjectType): the reference to the object that corresponds to the input
            arguments, regardless of whether it was found in the pool or not
        """
        key = self._build_hash(*args, **kwargs)
        if key not in self._objects:
            self._objects[key] = self.constructor(*args, **kwargs)
        return self._objects[key]
