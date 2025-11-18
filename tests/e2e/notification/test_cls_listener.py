from software_patterns import Subject


def test_classmethod_listener():
    class ClientObserver:
        updated = False

        @classmethod
        def update(cls, subject):
            cls.updated = True

    subject = Subject([])
    # Attach static/class methods directly
    subject.add(*[ClientObserver])

    # WHEN subject notifies
    subject.notify()

    # THEN static/class method is called
    assert ClientObserver.updated


def test_plan_classmethod_listener():
    class ClientObserver:
        updated = False

        @classmethod
        def update(cls, subject):
            cls.updated = True

    subject = Subject([])
    # Attach static/class methods directly
    subject.add(*[ClientObserver])

    # WHEN subject notifies
    subject.notify()

    # THEN static/class method is called
    assert ClientObserver.updated


def test_dynamic_class_listener():
    from software_patterns import Subject

    _state = 0

    def _update(subject):
        nonlocal _state
        _state += 1

    ClientObserver = type("Listener", (), {"update": _update})

    subject = Subject([])
    subject.attach(ClientObserver)

    # WHEN subject notifies
    subject.notify()

    # THEN instance method is called
    assert _state == 1
