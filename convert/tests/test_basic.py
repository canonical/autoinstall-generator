
from convert import convert


def test_di_locale_en_US():
    actual = convert('d-i debian-installer/locale string en_US')
    expected = '''Welcome:\n  lang: en_US'''
    assert expected == actual


def test_di_locale_en_GB():
    actual = convert('d-i debian-installer/locale string en_GB')
    expected = '''Welcome:\n  lang: en_GB'''
    assert expected == actual
