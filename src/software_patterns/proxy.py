"""Proxy structural software pattern.

This module contains boiler-plate code to supply the Proxy structural software
design pattern, to the client code."""

from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

T = TypeVar('T')


__all__ = ['ProxySubject', 'Proxy']


class ProxySubjectInterfaceClass(type, Generic[T]):
    """Interfacing enabling classes to construct classes (instead of instances).

    Dynamically creates classes that represent a ProxySubjectInterface.
    The created classes automatically gain an abstract method with name given at
    creation time. The input name can match the desired named selected to a
    proxied object.

    For example in a scenario where you proxy a remote web server you might
    create ProxySubjectInterface with a 'make_request' abstract method where as
    in a scenario where the proxied object is a Tensorflow function you might
    name the abstract method as 'tensorflow'.

    Dynamically, creating a class (as this class allows) is useful to adjust to
    scenarios like the above.

    Args:
        Generic ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    def __new__(mcs, *args, **kwargs):
        def __init__(self, proxied_object):
            self._proxy_subject = proxied_object

        def object(self, *args, **kwargs) -> T:
            return self._proxy_subject

        return super().__new__(
            mcs,
            'ProxySubjectInterface',
            (ABC,),
            {
                '__init__': __init__,
                args[0]: object,
            },
        )


class ProxySubjectInterface(ABC, Generic[T]):
    """Proxy Subject interface holding the important 'request' operation.

    Declares common operations for both ProxySubject and
    the Proxy. As long as the client uses ProxySubject's interface, a proxy can
    be passed pass to it, instead of a real subject.
    """

    @abstractmethod
    def request(self, *args, **kwargs) -> T:
        raise NotImplementedError


class ProxySubject(ProxySubjectInterface, Generic[T]):
    """
    The ProxySubject contains some core business logic. Usually, ProxySubject are
    capable of doing some useful work which may also be very slow or sensitive -
    e.g. correcting input data. A Proxy can solve these issues without any
    changes to the ProxySubject's code.

    Example:

        >>> from software_patterns import ProxySubject
        >>> proxied_operation = lambda x: x + 1
        >>> proxied_operation(1)
        2

        >>> proxied_object = ProxySubject(proxied_operation)
        >>> proxied_object.request(1)
        2
    """

    def __init__(self, callback: Callable[..., T]):
        self._callback = callback

    def request(self, *args, **kwargs) -> T:
        return self._callback(*args, **kwargs)


class Proxy(ProxySubjectInterface, Generic[T]):
    """
    The Proxy has an interface identical to the ProxySubject.

    Example:

        >>> from software_patterns import Proxy
        >>> from software_patterns import ProxySubject

        >>> class ClientProxy(Proxy):
        ...  def request(self, *args, **kwargs):
        ...   args = [args[0] + 1]
        ...   result = super().request(*args, **kwargs)
        ...   result += 1
        ...   return result

        >>> proxied_operation = lambda x: x * 2
        >>> proxy_subject = ProxySubject(proxied_operation)
        >>> proxy_subject.request(3)
        6

        >>> proxy = ClientProxy(proxy_subject)
        >>> proxy.request(3)
        9
    """

    def __init__(self, proxy_subject: ProxySubject):
        self._proxy_subject = proxy_subject

    def request(self, *args, **kwargs) -> T:
        """
        The most common applications of the Proxy pattern are lazy loading,
        caching, controlling the access, logging, etc. A Proxy can perform one
        of these things and then, depending on the result, pass the execution to
        the same method in a linked ProxySubject object.
        """
        return self._proxy_subject.request(*args, **kwargs)
