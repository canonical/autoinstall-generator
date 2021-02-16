
from convert import Directive, ConversionType
from merging import merge, do_merge, coallesce
import pytest


def test_basic():
    a = {'a': 1}
    b = {'b': 2}
    expected = {
        'a': 1,
        'b': 2,
    }
    actual = do_merge(a, b)
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

    actual = do_merge(b, c)
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

    actual = do_merge(c, d)
    assert expected == actual


def test_invalid_int():
    # this one worked automatically, as we tried to index into an int
    one = {'a': 1}
    two = {'a': 2}
    with pytest.raises(TypeError):
        do_merge(one, two)


def test_invalid_array():
    # this one was designed to fail where the int indexing didn't
    one = {'a': [1]}
    two = {'a': [2]}
    with pytest.raises(TypeError):
        do_merge(one, two)


def test_list():
    a = Directive({'a': 1}, '', ConversionType.UnknownError)
    b = Directive({'b': 2}, '', ConversionType.UnknownError)
    c = Directive({'c': 3}, '', ConversionType.UnknownError)
    expected = {
        'a': 1,
        'b': 2,
        'c': 3,
    }

    actual = merge([a, b, c])
    assert expected == actual


def test_coallesce():
    hostname = Directive({}, '', ConversionType.Dependent)
    directory = Directive({}, '', ConversionType.Dependent)
    hostname.fragments = {'mirror/http': {'hostname': 'asdf'}}
    directory.fragments = {'mirror/http': {'directory': '/qwerty'}}

    directives = [hostname, directory]

    actual = coallesce(directives)
    # expected_tree = {'apt': {
    #                     'primary': [{
    #                         'arches': ['default'],
    #                         'uri': f'http://asdf/qwerty'}]}}
    assert ConversionType.Coallesced == actual.convert_type
    assert directives == actual.children
    # assert expected_tree == actual.tree
