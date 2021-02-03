
from convert import convert, Directive, ConversionType


def trivial(start, finish):
    directive = convert(start)
    expected = finish
    assert expected == directive.line
    assert ConversionType.OneToOne == directive.convert_type


def test_directive():
    orig = 'my input'
    output = 'my output'
    convert_type = ConversionType.PassThru
    directive = Directive(output, orig, convert_type)
    assert output == directive.line
    assert orig == directive.orig_input
    assert convert_type == directive.convert_type


def test_di_locale():
    # FIXME needs .UTF-8 at the end in all cases?
    for locale in ['en_US', 'en_GB']:
        trivial(f'd-i debian-installer/locale string {locale}',
                f'locale: {locale}')


def test_di_locale_extra_stuff():
    locale = 'zz_ZZ'
    trivial(f' d-i debian-installer/locale string {locale} ',
            f'locale: {locale}')


def test_comment():
    lines = [
        '#### Contents of the preconfiguration file (for buster)',
        '### Localization',
        '# Preseeding only locale sets language, country and locale.',
        '',
        ' ' * 4,
    ]
    for line in lines:
        directive = convert(line)
        assert line == directive.line
        assert ConversionType.PassThru == directive.convert_type


def test_di_keymap():
    # d-i keyboard-configuration/xkb-keymap select us
    # keyboard:
    #   layout: gb
    for keymap in ['us', 'zz']:
        trivial(f'd-i keyboard-configuration/xkb-keymap select {keymap}',
                f'keyboard:\n  layout: {keymap}')


def test_di_invalid():
    line = 'd-i stuff/things string asdf'
    directive = convert(line)
    assert '' == directive.line
    assert ConversionType.UnknownError == directive.convert_type


def test_di_user_fullname():
    value = 'Debian User'
    # identity:
    #   realname: ''
    trivial(f'd-i passwd/user-fullname string {value}',
            f'identity:\n  realname: {value}')


def test_di_username():
    value = 'debian'
    # username: ubuntu
    trivial(f'd-i passwd/username string {value}',
            f'identity:\n  username: {value}')


def test_di_user_password_crypted():
    value = '$6$wdAcoXrU039hKYPd$508Qvbe7ObUnxoj15DRCkzC3qO7edjH0VV7BPNRDYK4' \
            'QR8ofJaEEF2heacn0QgD.f8pO8SNp83XNdWG6tocBM1'
    # password: '$6$wdAcoXrU039hKYPd$508Qvbe...'
    trivial(f'd-i passwd/user-password-crypted string {value}',
            f'identity:\n  password: {value}')


def test_di_hostname():
    value = 'somehost'
    # hostname: ubuntu
    trivial(f'd-i netcfg/hostname string {value}',
            f'identity:\n  hostname: {value}')
