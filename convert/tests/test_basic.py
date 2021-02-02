
from convert import convert


def test_di_locale():
    for locale in ['en_US', 'en_GB']:
        line = f'd-i debian-installer/locale string {locale}'
        actual = convert(line)
        expected = f'Welcome:\n  lang: {locale}'
        assert expected == actual

def test_comment():
    for line in ['', '# stuff things']:
        actual = convert(line)
        expected = line
        assert expected == actual


