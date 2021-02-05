
from merging import merge
import pytest


def test_basic():
    a = {'a': 1}
    b = {'b': 2}
    expected = {
        'a': 1,
        'b': 2,
    }
    actual = merge(a, b)
    assert expected == actual


def test_firstlevel():
    b = {'a': {'b': 1}}
    c = {'a': {'c': 2}}

    expected = {
        'a': {
            'b': 1,
            'c': 2,
        }
    }

    actual = merge(b, c)
    assert expected == actual


def test_secondlevel():
    c = {'a': {'b': {'c': 1}}}
    d = {'a': {'b': {'d': 2}}}
    expected = {
        'a': {
            'b': {
                'c': 1,
                'd': 2,
            }
        }
    }

    actual = merge(c, d)
    assert expected == actual


def test_invalid_int():
    # this one worked automatically, as we tried to index into an int
    one = {'a': 1}
    two = {'a': 2}
    with pytest.raises(TypeError):
        merge(one, two)


def test_invalid_array():
    # this one was designed to fail where the int indexing didn't
    one = {'a': [1]}
    two = {'a': [2]}
    with pytest.raises(TypeError):
        merge(one, two)
