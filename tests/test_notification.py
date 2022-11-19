import pytest

from software_patterns import Observer, Subject


def test_observers_sanity_test():
    subject1: Subject = Subject([])
    subject2: Subject = Subject([])
    assert hasattr(subject1, '_observers')
    assert hasattr(subject2, '_observers')
    assert id(subject1._observers) != id(subject2._observers)


# def test_observer_as_constructor(observer: t.Type[Observer]):
def test_observer_as_constructor():
    observer = Observer

    with pytest.raises(TypeError) as instantiation_from_interface_error:
        _observer_instance = observer()  # type: ignore[abstract]

    import re

    runtime_exception_message_reg = (
        "Can't instantiate abstract class " "Observer with abstract methods? update"
    )

    assert re.match(
        runtime_exception_message_reg, str(instantiation_from_interface_error.value)
    )


# def test_scenario(subject: t.Type[Subject], observer: t.Type[Observer]):
def test_scenario():
    # Scenario 1
    # The client code.
    class ObserverA(Observer):
        def update(self, *args, **kwargs) -> None:
            print("ObserverA: Reacted to the event")

    s1: Subject = Subject([])
    o1 = ObserverA()
    s1.attach(o1)

    # business logic
    s1.state = 0
    s1.notify()

    # Scenario 2
    class Businessubject(Subject):
        def some_business_logic(self) -> None:
            """
            Usually, the subscription logic is only a fraction of what a Subject can
            really do. Subjects commonly hold some important business logic, that
            triggers a notification method whenever something important is about to
            happen (or after it).
            """
            print("\nSubject: I'm doing something important.")
            self._state = 2
            print(f"Subject: My state has just changed to: {self._state}")
            self.notify()

    class ObserverB(Observer):
        def update(self, *args, **kwargs) -> None:
            subject = args[0]
            if subject.state == 0 or subject.state >= 2:
                print("ObserverB: Reacted to the event")

    s2 = Businessubject([])
    assert id(s1) != id(s2)
    assert id(s1._observers) != id(s2._observers)
    o1, o2 = ObserverA(), ObserverB()

    s2.add(o1, o2)
    # business logic
    print(s2._observers)
    s2.some_business_logic()
    s2.some_business_logic()

    s2.detach(o1)
    s2.some_business_logic()
