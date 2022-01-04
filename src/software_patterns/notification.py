"""Notification-Listener (aka subject-observer) software design pattern.

Simple implementation of the subject/observers (broadcast/listeners) pattern,
exposed as python classes.

This is a Behavioural Pattern which can be used when you want one or more
components to be notified and react accordingly, when 'something happens'.

One entity, known as Subject, is responsible to send out a notification and each
entity "subscribed" to the Subject receives it and reacts.
Each subscribed entity is known as a Listener or Observer.

The idea is that the Subject is agnostic of its Observers implementation and the
client code can "attach" or "detach" (subscribe/unsubscribe) as many of them at
runtime.

This module provides the Observer class, serving as the interface that needs to
be implemented by concrete classes; the update method needs to be overrode.
Concrete Observers react to the notifications/updates issued by the Subject they
had been attached/subscribed to.

This module also provides the concrete Subject class, serving with methods to
subscribe/unsubscribe (attach/detach) observers and also with a method to
"notify" all Observers.
"""

from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar

__all__ = ['Subject', 'Observer']


StateType = TypeVar('StateType')


class ObserverInterface(ABC):
    """The Observer interface declares the update method, used by subjects.

    Enables objects to act as "event" listeners; react to "notifications"
    by executing specific (event) handling logic.
    """
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Receive an update (from a subject); handle an event notification."""
        raise NotImplementedError


class SubjectInterface(ABC):
    """The Subject interface declares a set of methods for managing subscribers.

    Enables objects to act as subjects that broadcast events" by notifying
    all subscribed observers/listeners.
    """

    @abstractmethod
    def attach(self, observer: ObserverInterface) -> None:
        """Attach an observer to the subject; subscribe the observer."""
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer: ObserverInterface) -> None:
        """Detach an observer from the subject; unsubscribe the observer."""
        raise NotImplementedError

    @abstractmethod
    def notify(self) -> None:
        """Notify all observers about an event."""
        raise NotImplementedError


class Observer(ObserverInterface, ABC):
    pass


class Subject(SubjectInterface, Generic[StateType]):
    """Concrete Subject which owns an important state and notifies observers.

    The subject can be used to build the data encapsulating the event being
    broadcasted.

    Both the _state and _observers attributes have a simple implementation,
    but can be overrode to accommodate for more complex scenarios.

    The observers/subscribers are implemented as a python list.
    In more complex scenarios, the list of subscribers can
    be stored more comprehensively (categorized by event type, etc.).

    The subscription management methods provided are 'attach', 'detach' (as in
    the SubjectInterface) and 'add', which attached multiple observers at once.

    Example:

        >>> from software_patterns import Subject, Observer

        >>> broadcaster = Subject()

        >>> class ObserverTypeA(Observer):
        ...  def update(self, *args, **kwargs):
        ...   event = args[0].state
        ...   print(f'observer-type-a reacts to event {event}')

        >>> class ObserverTypeB(Observer):
        ...  def update(self, *args, **kwargs):
        ...   event = args[0].state
        ...   print(f'observer-type-b reacts to event {event}')

        >>> subscriber_1 = ObserverTypeA()
        >>> subscriber_2 = ObserverTypeB()

        >>> broadcaster.add(subscriber_2, subscriber_1)

        >>> broadcaster.state = 'event-object-A'

        >>> broadcaster.notify()
        observer-type-b reacts to event event-object-A
        observer-type-a reacts to event event-object-A

        >>> broadcaster.detach(subscriber_2)

        >>> broadcaster.state = 'event-object-B'
        >>> broadcaster.notify()
        observer-type-a reacts to event event-object-B
    """
    def __init__(self, *args, **kwargs):
        self._observers: List[ObserverInterface] = []
        self._state = None

    def attach(self, observer: ObserverInterface) -> None:
        self._observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def add(self, *observers):
        """Subscribe multiple observers at once."""
        self._observers.extend(list(observers))

    @property
    def state(self) -> StateType:
        """Get the state of the Subject.

        Returns:
            StateType: the object representing the current state of the Subject
        """
        return self._state

    @state.setter
    def state(self, state: StateType):
        """Set the state of the Subject.

        Args:
            state (StateType): the state object
        """
        self._state = state
