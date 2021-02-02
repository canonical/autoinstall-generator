
from convert import Answer, convert


def test_answer():
    line = 'stuff'
    actual = Answer(line).line
    expected = line
    assert expected == actual


def test_di_locale():
    for locale in ['en_US', 'en_GB']:
        line = f'd-i debian-installer/locale string {locale}'
        actual = convert(line)
        expected = f'Welcome:\n  lang: {locale}'
        assert expected == actual


def test_di_locale_extra_stuff():
    locale = 'zz_ZZ'
    line = f' d-i debian-installer/locale string {locale} # locale comment'
    actual = convert(line)
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
        actual = convert(line)
        expected = line
        assert expected == actual
