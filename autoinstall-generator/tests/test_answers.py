
from answers import convert, Answer, ConversionType


def trivial(start, finish):
    answer = convert(start)
    expected = finish
    assert expected == answer.line
    assert ConversionType.OneToOne == answer.convert_type


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
        trivial(f'd-i debian-installer/locale string {locale}',
                f'Welcome:\n  lang: {locale}')


def test_di_locale_extra_stuff():
    locale = 'zz_ZZ'
    trivial(f' d-i debian-installer/locale string {locale} ',
            f'Welcome:\n  lang: {locale}')


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


def test_di_keymap():
    # d-i keyboard-configuration/xkb-keymap select us
    # Keyboard:
    #   layout: us
    for keymap in ['us', 'zz']:
        trivial(f'd-i keyboard-configuration/xkb-keymap select {keymap}',
                f'Keyboard:\n  layout: {keymap}')


def test_di_invalid():
    line = 'd-i stuff/things string asdf'
    answer = convert(line)
    assert '' == answer.line
    assert ConversionType.UnknownError == answer.convert_type


def test_di_user_fullname():
    value = 'Debian User'
    trivial(f'd-i passwd/user-fullname string {value}',
            f'Identity:\n  realname: {value}')


def test_di_username():
    value = 'debian'
    trivial(f'd-i passwd/username string {value}',
            f'Identity:\n  username: {value}')


def test_di_user_password_crypted():
    value = '$6$wdAcoXrU039hKYPd$508Qvbe7ObUnxoj15DRCkzC3qO7edjH0VV7BPNRDYK4' \
            'QR8ofJaEEF2heacn0QgD.f8pO8SNp83XNdWG6tocBM1'
    trivial(f'd-i passwd/user-password-crypted string {value}',
            f'Identity:\n  password: {value}')


def test_di_hostname():
    value = 'somehost'
    trivial(f'd-i netcfg/hostname string {value}',
            f'Identity:\n  hostname: {value}')
