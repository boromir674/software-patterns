from software_patterns import Subject, Observer


def test_static_listener():
    class ClientObserver(Observer):
        updated = False

        @staticmethod
        def update(subject):
            ClientObserver.updated = True

    subject = Subject([])
    # Attach static/class methods directly
    subject.add(*[ClientObserver])

    # WHEN subject notifies
    subject.notify()

    # THEN static/class method is called
    assert ClientObserver.updated



def test_plain_static_listener():
    class ClientObserver:
        updated = False

        @staticmethod
        def update(subject):
            ClientObserver.updated = True

    subject = Subject([])
    # Attach static/class methods directly
    subject.add(*[ClientObserver])

    # WHEN subject notifies
    subject.notify()

    # THEN static/class method is called
    assert ClientObserver.updated
