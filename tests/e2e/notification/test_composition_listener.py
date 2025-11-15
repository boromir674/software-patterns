import pytest


def test_namedtuple_listener():
    from collections import namedtuple

    from software_patterns import Subject

    _state = 0

    def _update(subject):
        nonlocal _state
        _state += 1

    listener = namedtuple("Listener", ["update"])(_update)

    subject = Subject([])
    subject.attach(listener)

    # WHEN subject notifies
    subject.notify()

    # THEN instance method is called
    assert _state == 1


def test_encapsulated_listener():
    from software_patterns import Observer, Subject

    # GIVEN a client class with Subject as attribute
    class ClientObserver(Observer):
        def __init__(self):
            self.updated = False
            self.subject = Subject([])
            self.subject.attach(self)

        def update(self, subject):
            self.updated = True

    client = ClientObserver()

    # WHEN client’s subject notifies
    client.subject.notify()

    # THEN instance method is called
    assert client.updated


def test_composition_with_incompatible_listener():
    from software_patterns import Subject

    # GIVEN a client class with Subject as attribute
    class ClientObserver:
        def __init__(self):
            self.updated = False
            self.subject = Subject([])
            self.subject.attach(self)

        # GIVEN the object doe NOT have a compatible 'update' method
        def update_with_typo(self, subject): ...

    # THEN attaching the incompatible listener raises TypeError, with expected message
    with pytest.raises(
        TypeError, match="Attached observer .* does not have a callable 'update' method."
    ):
        _client = ClientObserver()
