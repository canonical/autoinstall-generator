
from convert import convert, Directive, ConversionType
from merging import merge, do_merge, coalesce, bucketize, Bucket
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


def test_redundant():
    a = {'a': 1}
    expected = {
        'a': 1,
    }
    actual = do_merge(a, a)
    assert expected == actual


def test_redundant_array():
    a = {'a': [1]}
    expected = {
        'a': [1],
    }
    actual = do_merge(a, a)
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


def test_coalesce():
    hostname = 'asdf'
    directory = '/qwerty'
    lines = [
        f'd-i mirror/http/hostname string {hostname}',
        f'd-i mirror/http/directory string {directory}',
    ]

    directives = []
    for line in lines:
        directives.append(convert(line))

    actual = coalesce(directives)
    expected_tree = {
        'apt': {
            'primary': [{
                'arches': ['default'],
                'uri': f'http://{hostname}{directory}',
            }]
        }
    }
    expected_fragments = {
        'mirror/http': {
            'hostname': hostname,
            'directory': directory,
        }
    }
    assert ConversionType.Coalesced == actual.convert_type
    assert directives == actual.children
    assert expected_fragments == actual.fragments
    assert expected_tree == actual.tree


def test_bucketize():
    # bucketization is the process by which directives are processed to
    # determine if they are standalone or if they require coalescing.
    lines = [
        'd-i mirror/http/hostname string a',
        'd-i mirror/http/directory string /b',
        'd-i debian-installer/locale string en_US',
    ]
    key = 'mirror/http'

    directives = [convert(line) for line in lines]
    buckets = bucketize(directives)
    assert 1 == len(buckets.independent)
    assert ConversionType.OneToOne == buckets.independent[0].convert_type
    assert 1 == len(buckets.dependent)
    assert key in buckets.dependent
    assert 2 == len(buckets.dependent[key])
    for d in buckets.dependent[key]:
        assert ConversionType.Dependent == d.convert_type


def test_coalesce_buckets():
    buckets = Bucket()
    lines = [
        'd-i mirror/http/hostname string a',
        'd-i mirror/http/directory string /b',
    ]
    key = 'mirror/http'
    directives = [convert(line) for line in lines]
    buckets.dependent[key] = directives

    coalesced = buckets.coalesce()

    assert 1 == len(coalesced)
    assert ConversionType.Dependent != coalesced[0].convert_type
