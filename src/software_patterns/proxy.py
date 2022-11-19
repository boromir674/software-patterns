"""Proxy structural software pattern.

This module contains boiler-plate code to supply the Proxy structural software
design pattern, to the client code."""

from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')


__all__ = ['Proxy']


class ProxySubjectInterface(ABC):
    """Proxy Subject interface holding the important 'request' operation.

    Declares common operations for both ProxySubject and
    the Proxy. As long as the client uses ProxySubject's interface, a proxy can
    be passed pass to it, instead of a real subject.
    """


class Proxy(ProxySubjectInterface, Generic[T]):
    """
    The Proxy has an interface identical to the ProxySubject.

    Example:

        >>> from software_patterns import Proxy
        >>> class PlusTen(Proxy):
        ...  def __call__(self, x: int):
        ...   result = self._proxy_subject(x + 10)
        ...   return result

        >>> def plus_one(x: int):
        ...  return x + 1
        >>> plus_one(2)
        3

        >>> proxy = PlusTen(plus_one)
        >>> proxy(2)
        13
    """

    def __init__(self, runtime_proxy: T):
        self._proxy_subject = runtime_proxy

    def __getattr__(self, name: str):
        return getattr(self._proxy_subject, name)

    def __str__(self):
        return str(self._proxy_subject)

    def __hash__(self):
        return hash(self._proxy_subject)
