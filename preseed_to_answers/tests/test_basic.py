
from convert import *


def test_answer():
    orig = 'my input'
    output = 'my output'
    convert_type = ConversionType.PassThru
    answer = Answer(output, orig, convert_type)
    assert output == answer.line
    assert orig == answer.orig_input
    assert convert_type == answer.convert_type


def test_di_locale():
    for locale in ['en_US', 'en_GB']:
        line = f'd-i debian-installer/locale string {locale}'
        answer = convert(line)
        expected = f'Welcome:\n  lang: {locale}'
        assert expected == answer.line
        assert ConversionType.OneToOne == answer.convert_type


def test_di_locale_extra_stuff():
    locale = 'zz_ZZ'
    line = f' d-i debian-installer/locale string {locale} # locale comment'
    actual = convert(line).line
    expected = f'Welcome:\n  lang: {locale}'
    assert expected == actual


def test_comment():
    lines = [
        '#### Contents of the preconfiguration file (for buster)',
        '### Localization',
        '# Preseeding only locale sets language, country and locale.',
        '',
        ' ' * 4,
    ]
    for line in lines:
        answer = convert(line)
        assert line == answer.line
        assert ConversionType.PassThru == answer.convert_type
