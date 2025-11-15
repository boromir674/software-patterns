from software_patterns import Subject, Observer


def test_composition_listener():
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


def test_composition_listener2():
    # GIVEN a client class with Subject as attribute
    class ClientObserver:
        def __init__(self):
            self.updated = False
            self.subject = Subject([])
            self.subject.attach(self)
        def update1(self, subject):
            self.updated = True

    client = ClientObserver()

    # WHEN client’s subject notifies
    client.subject.notify()

    # THEN instance method is called
    assert client.updated
