__version__ = '1.2.1'

from .memoize import ObjectsPool
from .notification import Observer, Subject
from .proxy import Proxy, ProxySubject
from .singleton import Singleton
from .subclass_registry import SubclassRegistry

__all__ = [
    'Observer',
    'Subject',
    'ObjectsPool',
    'SubclassRegistry',
    'ProxySubject',
    'Proxy',
    'Singleton',
]
