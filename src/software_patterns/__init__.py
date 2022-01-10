__version__ = '1.0.0'

from .notification import Observer, Subject
from .memoize import ObjectsPool
from .proxy import ProxySubject, Proxy
from .subclass_registry import SubclassRegistry


__all__ = ['Observer', 'Subject', 'ObjectsPool', 'SubclassRegistry',
    'ProxySubject', 'Proxy']
