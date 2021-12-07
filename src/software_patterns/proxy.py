"""Proxy structural software pattern.

This module contains boiler-plate code to supply the Proxy structural software
design pattern, to the client code."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


__all__ = ['ProxySubject', 'Proxy']


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
    """

    def request(self, *args, **kwargs) -> T:
        raise NotImplementedError


class Proxy(ProxySubjectInterface, Generic[T]):
    """
    The Proxy has an interface identical to the ProxySubject.
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
