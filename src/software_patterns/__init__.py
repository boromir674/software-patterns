__version__ = '0.9.0'

from .notification import Observer, Subject
from .memoize import ObjectsPool
from .proxy import ProxySubject, Proxy
from .subclass_registry import SubclassRegistry


__all__ = ['Observer', 'Subject', 'ObjectsPool', 'SubclassRegistry',
    'ProxySubject', 'Proxy']
