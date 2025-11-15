from software_patterns import Subject, Observer

def test_event_data_passing():
    class EventObserver(Observer):
        def __init__(self):
            self.received_data = None
        def update(self, subject):
            # Try to access event data
            self.received_data = getattr(subject, 'event_data', None)

    subject = Subject([])
    observer = EventObserver()
    subject.attach(observer)

    # Set event data on subject
    subject.event_data = {'type': 'custom', 'payload': 42}
    subject.notify()

    assert observer.received_data == {'type': 'custom', 'payload': 42}
