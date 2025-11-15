import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_listener():
    from software_patterns import Subject, Observer

    class AsyncObserver(Observer):
        def __init__(self):
            self.called = False
        async def update(self, subject):
            await asyncio.sleep(0.01)
            self.called = True

    subject = Subject([])
    observer = AsyncObserver()
    subject.attach(observer)

    await subject.notify_async()
    assert observer.called


@pytest.mark.asyncio
async def test_ducktype_async_listener():
    from software_patterns import Subject

    class AsyncObserver:
        def __init__(self):
            self.called = False
        async def update(self, subject):
            await asyncio.sleep(0.01)
            self.called = True

    subject = Subject([])
    observer = AsyncObserver()
    subject.attach(observer)

    await subject.notify_async()
    assert observer.called



@pytest.mark.asyncio
async def test_incompatible_async_listener():
    from software_patterns import Subject

    class IncompatibleAsyncObserver:
        def __init__(self):
            self.called = False
        async def update_with_typo(self, subject):
            await asyncio.sleep(0.01)
            self.called = True

    subject = Subject([])
    observer = IncompatibleAsyncObserver()
    with pytest.raises(TypeError, match="Attached observer .* does not have a callable 'update' method."):
        subject.attach(observer)

    # await subject.notify_async()
    # assert observer.called
