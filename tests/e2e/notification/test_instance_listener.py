from software_patterns import Observer, Subject


def test_instance_listener():
    # GIVEN a client class with an update method
    class ClientObserver(Observer):
        def __init__(self):
            self.updated = False

        def update(self, subject):
            self.updated = True

    listener = ClientObserver()

    subject = Subject([])
    subject.attach(listener)

    # WHEN subject notifies
    subject.notify()

    # THEN instance method is called
    assert listener.updated


def test_plain_instance_listener():
    # GIVEN a client class with an update method
    class ClientObserver:
        def __init__(self):
            self.updated = False

        def update(self, subject):
            self.updated = True

    listener = ClientObserver()

    subject = Subject([])
    subject.attach(listener)

    # WHEN subject notifies
    subject.notify()

    # THEN instance method is called
    assert listener.updated


def test_dynamic_class_instance_listener():
    from software_patterns import Subject

    _state = 0

    def _update(self, subject):
        nonlocal _state
        _state += 1

    listener = type("Listener", (), {"update": _update})()

    subject = Subject([])
    subject.attach(listener)

    # WHEN subject notifies
    subject.notify()

    # THEN instance method is called
    assert _state == 1
