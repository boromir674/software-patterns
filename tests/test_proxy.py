import pytest


@pytest.fixture
def dummy_handle():
    def handle(self, *args, **kwargs):
        return f'{type(self).__name__} handle request with args [{", ".join((str(_) for _ in args))}] and kwargs [{", ".join(f"{k}={v}" for k, v in kwargs.items())}]'

    return handle


def test_proxy_behaviour(dummy_handle, capsys):
    from typing import List

    from software_patterns import Proxy

    # replicate client code that wants to use the proxy pattern
    class ClientSubject(object):
        """ "A class with a request instance method."""

        def request(self, *args, **kwargs):
            print(dummy_handle(self, *args, **kwargs))
            return type(self).__name__

    # Derive from Proxy
    class ClientProxy(Proxy):
        def request(self, *args, **kwargs):

            # run proxy code before sending request to the "proxied" handler
            before_args = list(['before'] + list(args))
            print(dummy_handle(self, *before_args, **kwargs))
            # handle request with the proxied logic
            # _ = super().request(*args, **kwargs)
            _ = self._proxy_subject.request(*args, **kwargs)
            assert _ == 'ClientSubject'

            # run proxy code after request to the "proxied" handler
            after_args = list(['after'] + list(args))
            print(dummy_handle(self, *after_args, **kwargs))
            return _

    real_subject = ClientSubject()
    proxy = ClientProxy(real_subject)

    # use proxy in a scenario

    # First test what happens without using proxy
    args: List = [1, 2]
    kwargs = {'k1': 'v1'}
    result = real_subject.request(*args, **kwargs)

    captured = capsys.readouterr()
    assert captured.out == dummy_handle(real_subject, 1, 2, k1='v1') + '\n'
    assert (
        captured.out
        == f'ClientSubject handle request with args [{", ".join(str(_) for _ in args)}] and kwargs [{", ".join(f"{k}={v}" for k, v in kwargs.items())}]\n'
    )
    assert result == type(real_subject).__name__
    assert result == 'ClientSubject'

    # Now test what happens using proxy
    result = proxy.request(*args, **kwargs)

    captured = capsys.readouterr()

    assert (
        captured.out
        == dummy_handle(*list([proxy, 'before'] + args), **kwargs)
        + '\n'
        + dummy_handle(*list([real_subject] + args), **kwargs)
        + '\n'
        + dummy_handle(*list([proxy, 'after'] + args), **kwargs)
        + '\n'
    )
    assert (
        captured.out
        == f'ClientProxy handle request with args [{", ".join(str(_) for _ in ["before"] + args)}] and kwargs [{", ".join(f"{k}={v}" for k, v in kwargs.items())}]\n'
        + f'ClientSubject handle request with args [{", ".join(str(_) for _ in args)}] and kwargs [{", ".join(f"{k}={v}" for k, v in kwargs.items())}]\n'
        + f'ClientProxy handle request with args [{", ".join(str(_) for _ in ["after"] + args)}] and kwargs [{", ".join(f"{k}={v}" for k, v in kwargs.items())}]\n'
    )
    assert result == type(real_subject).__name__
    assert result == 'ClientSubject'


def test_simple_proxy():
    from typing import Callable

    from software_patterns import Proxy

    RemoteCall = Callable[[int], int]
    remote_call: RemoteCall = lambda x: x + 1

    # Code that the developer writes
    VALUE = 10

    class ClientProxy(Proxy[RemoteCall]):
        def __call__(self, x: int):
            return self._proxy_subject(x + VALUE)

    proxy: ClientProxy = ClientProxy(remote_call)

    assert remote_call(2) == 2 + 1
    assert proxy(2) == 2 + VALUE + 1


def test_proxy_as_instance():
    from typing import Callable

    from software_patterns import Proxy

    RemoteCall = Callable[[int], int]

    remote_call: RemoteCall = lambda x: x + 1

    # Code that the developer writes
    VALUE = 10

    class ClientProxy(Proxy[RemoteCall]):
        def __call__(self, x: int):
            return self._proxy_subject(x + VALUE)

    proxy: ClientProxy = ClientProxy(remote_call)

    assert remote_call(2) == 2 + 1
    assert proxy(2) == 2 + VALUE + 1

    assert hash(proxy) == hash(remote_call)


def test_mapping_proxy():
    from typing import Mapping

    from software_patterns import Proxy

    # test data
    RemoteMapping = Mapping[str, str]

    remote_mapping: RemoteMapping = {
        'id_1': 'a',
        'id_2': 'b',
    }

    ## Code that the developer writes

    class ClientProxy(Proxy[Mapping]):
        CACHE = {
            'id_1': 'a-cached',
        }

        def __getitem__(self, str_id: str):
            return self.CACHE.get(str_id, self._proxy_subject[str_id])

        def __contains__(self, element):
            return element in self._proxy_subject

        def wipe_cache(self):
            self.CACHE = {}

    proxy: ClientProxy = ClientProxy(remote_mapping)

    # Test code
    assert remote_mapping['id_1'] == 'a'
    assert remote_mapping['id_2'] == 'b'
    assert 'id_1' in remote_mapping

    assert proxy['id_1'] == 'a-cached'
    assert proxy['id_2'] == 'b'
    assert 'id_1' in proxy

    # Proxy delegates attribute requests (ie 'keys' as below) to subject
    assert sorted(remote_mapping.keys()) == sorted(proxy.keys())
    assert str(proxy) == str(remote_mapping)

    proxy.wipe_cache()

    assert proxy['id_1'] == 'a'
    assert proxy['id_2'] == 'b'
    assert sorted(remote_mapping.keys()) == sorted(proxy.keys())
    assert str(proxy) == str(remote_mapping)
