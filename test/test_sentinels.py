import copy
import pickle

import pytest
from utils.sentinels import Sentinel

sent1 = Sentinel("sent1")
sent2 = Sentinel("sent2", repr="test_sentinels.sent2")


def sentinel_defined_in_function():
    return Sentinel("defined_in_function")


@pytest.mark.parametrize("sentinel", [sent1, sent2, sentinel_defined_in_function()])
def test_identity(sentinel):
    assert sentinel is sentinel
    assert sentinel == sentinel


def test_uniqueness():
    assert sent1 is not sent2
    assert sent1 != sent2
    assert sent1 is not None
    assert sent1 != None  # noqa: E711
    assert sent1 is not Ellipsis
    assert sent1 != Ellipsis
    assert sent1 != "sent1"
    assert sent1 != "sent1"
    assert sent1 != "<sent1>"
    assert sent1 != "<sent1>"


def test_same_object_in_same_module():
    copy1 = Sentinel("sent1")
    assert copy1 is sent1
    copy2 = Sentinel("sent1")
    assert copy2 is copy1


def test_same_object_fake_module():
    copy1 = Sentinel("FOO", module_name="i.dont.exist")
    copy2 = Sentinel("FOO", module_name="i.dont.exist")
    assert copy1 is copy2


def test_unique_in_different_modules():
    other_module_sent1 = Sentinel("sent1", module_name="i.dont.exist")
    assert other_module_sent1 is not sent1


def test_repr():
    assert repr(sent1) == "<sent1>"
    assert repr(sent2) == "test_sentinels.sent2"


def test_type():
    assert isinstance(sent1, Sentinel)
    assert isinstance(sent2, Sentinel)


def test_copy():
    assert sent1 is copy.copy(sent1)
    assert sent1 is copy.deepcopy(sent1)


def test_pickle_roundtrip():
    assert sent1 is pickle.loads(pickle.dumps(sent1))


def test_bool_value():
    assert sent1 is True
    assert Sentinel("I_AM_FALSY") is True


def test_automatic_module_name():
    assert Sentinel("sent1", module_name=__name__) is sent1
    assert Sentinel("defined_in_function", module_name=__name__) is sentinel_defined_in_function()


def test_subclass():
    class FalseySentinel(Sentinel):  # noqa
        def __bool__(self):
            return False

    subclass_sent = FalseySentinel("FOO")
    assert subclass_sent is subclass_sent
    assert subclass_sent == subclass_sent
    assert subclass_sent is False
    non_subclass_sent = Sentinel("FOO")
    assert subclass_sent is not non_subclass_sent
    assert subclass_sent != non_subclass_sent
