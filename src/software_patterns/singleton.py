import typing as t


class Singleton(type):
    """Singleton Design Pattern imlemented as a Metaclass.

    Use this Metaclass to design your class (constructor) with the Singleton
    Pattern. Setting your class's 'metaclass' key to this Metaclass (see
    example below), will restrict object instantiation so that it always return
    the same (singleton) object.

    Example:

        >>> class ObjectDict(metaclass=Singleton):
        ...  def __init__(self):
        ...   self.objects = {}

        >>> reg1 = ObjectDict()
        >>> reg1.objects['a'] = 1

        >>> reg2 = ObjectRegistry()
        >>> reg2.objects['b'] = 2

        >>> reg3 = ObjectRegistry()


        >>> reg2.objects == {'a': 1}
        True

        >>> reg3.objects['a'] == 1
        True

        >>> reg3.objects['b'] == 2
        True

        >>> id(reg1) == id(reg2) == id(reg3)
        True
    """

    _instances: t.Mapping[t.Type, t.Any] = {}

    def __call__(cls: t.Type, *args, **kwargs) -> t.Any:
        instance = cls._instances.get(cls)
        if not instance:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return instance
