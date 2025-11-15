import pytest


def test_static_listener():
    from software_patterns import Observer, Subject

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
    from software_patterns import Subject

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


def test_incompatible_listener_raises_typeerror():
    from software_patterns import Subject

    class ClientObserver:
        updated = False

    subject = Subject([])

    with pytest.raises(
        TypeError, match="Attached observer .* does not have a callable 'update' method."
    ):
        # Attach static/class methods directly
        subject.attach(ClientObserver)


def test_adding_good_and_bad_listeners_adds_the_compatible_ones():
    from software_patterns import Subject

    _state = {"count": 0}

    class CompatibleClientObserver:
        updated = False

        @staticmethod
        def update(subject):
            _state["count"] += 1

    class IncompatibleClientObserverWithTypo:
        @staticmethod
        def update_typo(subject):
            # This should not be called because it doesn't provide 'update'
            _state["count"] += 1

    class IncompatibleClientObserver:
        updated = False

    subject = Subject([])

    # Attach both compatible and incompatible observers
    subscription_result = subject.add(
        CompatibleClientObserver,
        IncompatibleClientObserverWithTypo,
        IncompatibleClientObserver,
    )

    # THEN the number of attached observers should be equal to 1, since we had 1 compatible observer
    assert len(subscription_result.added) == 1

    # AND the incompatible ones should be in the 'skipped' list
    assert len(subscription_result.failed) == 2

    # WHEN subject notifies
    subject.notify()

    # THEN only the compatible observer was called
    assert _state["count"] == 1
