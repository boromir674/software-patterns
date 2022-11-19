__version__ = '1.3.0'

from .memoize import ObjectsPool
from .notification import Observer, Subject
from .proxy import Proxy
from .singleton import Singleton
from .subclass_registry import SubclassRegistry

__all__ = [
    'Observer',
    'Subject',
    'ObjectsPool',
    'SubclassRegistry',
    'Proxy',
    'Singleton',
]
