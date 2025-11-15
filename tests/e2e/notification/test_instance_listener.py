from software_patterns import Observer, Subject


def test_instance_listener():
    # GIVEN a client class with an update method
    class ClientObserver(Observer):
        def __init__(self):
            self.updated = False

        def update(self, subject):
            self.updated = True

    client = ClientObserver()

    subject = Subject([])
    subject.attach(client)

    # WHEN subject notifies
    subject.notify()

    # THEN instance method is called
    assert client.updated


def test_plain_instance_listener():
    # GIVEN a client class with an update method
    class ClientObserver:
        def __init__(self):
            self.updated = False

        def update(self, subject):
            self.updated = True

    client = ClientObserver()

    subject = Subject([])
    subject.attach(client)

    # WHEN subject notifies
    subject.notify()

    # THEN instance method is called
    assert client.updated
