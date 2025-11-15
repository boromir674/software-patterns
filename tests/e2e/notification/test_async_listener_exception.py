import pytest

from software_patterns import Observer, Subject


@pytest.mark.asyncio
async def test_async_listener_exception_good_bad():
    class GoodAsyncObserver(Observer):
        def __init__(self):
            self.called = False

        async def update(self, subject):
            self.called = True

    class BadAsyncObserver(Observer):
        async def update(self, subject):
            raise RuntimeError("Async listener error!")

    subject = Subject([])
    good = GoodAsyncObserver()
    bad = BadAsyncObserver()
    subject.add(good, bad)

    with pytest.raises(RuntimeError, match="Async listener error!"):
        await subject.notify_async()
    assert good.called


@pytest.mark.asyncio
async def test_async_listener_allows_updates_even_though_some_might_fail():
    class GoodAsyncObserver(Observer):
        def __init__(self):
            self.called = False

        async def update(self, subject):
            self.called = True

    class BadAsyncObserver(Observer):
        async def update(self, subject):
            raise RuntimeError("Async listener error!")

    subject = Subject([])
    good = GoodAsyncObserver()
    bad = BadAsyncObserver()
    subject.add(bad, good)

    with pytest.raises(RuntimeError, match="Async listener error!"):
        await subject.notify_async()
    assert good.called
