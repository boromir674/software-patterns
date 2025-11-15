import pytest

from software_patterns import Observer, Subject


def test_sync_listener_exception():
    class GoodObserver(Observer):
        def __init__(self):
            self.called = False

        def update(self, subject):
            self.called = True

    class BadObserver(Observer):
        def update(self, subject):
            raise ValueError("Listener error!")

    subject = Subject([])
    good = GoodObserver()
    bad = BadObserver()
    subject.add(good, bad)

    assert not good.called
    with pytest.raises(ValueError, match="Listener error!"):
        subject.notify()

    assert good.called


def test_sync_listener_order_matters_exception():
    class GoodObserver(Observer):
        def __init__(self):
            self.called = False

        def update(self, subject):
            self.called = True

    class BadObserver(Observer):
        def update(self, subject):
            raise ValueError("Listener error!")

    subject = Subject([])
    good = GoodObserver()
    bad = BadObserver()
    subject.add(bad, good)

    assert not good.called
    with pytest.raises(ValueError, match="Listener error!"):
        subject.notify()

    assert not good.called


def test_sync_listener_try_exception():
    class GoodObserver(Observer):
        def __init__(self):
            self.called = False

        def update(self, subject):
            self.called = True

    class BadObserver(Observer):
        def update(self, subject):
            raise ValueError("Listener error!")

    subject = Subject([])
    good = GoodObserver()
    bad = BadObserver()
    subject.add(good, bad)

    assert not good.called
    try:
        subject.notify()
    except ValueError as e:
        print(e)

    assert good.called


def test_sync_listener_order_matters_try_exception():
    class GoodObserver(Observer):
        def __init__(self):
            self.called = False

        def update(self, subject):
            self.called = True

    class BadObserver(Observer):
        def update(self, subject):
            raise ValueError("Listener error!")

    subject = Subject([])
    good = GoodObserver()
    bad = BadObserver()
    subject.add(bad, good)

    assert not good.called
    try:
        subject.notify()
    except ValueError as e:
        print(e)

    assert not good.called
