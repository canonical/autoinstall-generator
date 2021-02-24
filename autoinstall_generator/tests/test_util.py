
from autoinstall_generator.convert import is_multiline, prefixify


def test_is_multiline():
    assert is_multiline('a\nb\nc\n')
    assert is_multiline('a\nb\n')
    assert not is_multiline('a\n')


def test_commentize():
    data = 'a\nb\nc\n'
    expected = '# a\n# b\n# c\n'
    assert expected == prefixify(data)


def test_prefixify():
    data = 'a\nb\nc\n'
    expected = '//a\n//b\n//c\n'
    assert expected == prefixify(data, '//')


def test_first_prefixify():
    data = 'a\nb\nc\n'
    expected = '// a\n   b\n   c\n'
    assert expected == prefixify(data, '   ', '// ')
