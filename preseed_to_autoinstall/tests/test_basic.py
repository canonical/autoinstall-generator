
from convert import (convert, Directive, ConversionType, netmask_bits,
                     insert_at_none)
import pytest


# FIXME actually generate files
# FIXME leader version
# FIXME dependency support - to handle ipaddress / netmask


def trivial(start, finish):
    directive = convert(start)
    expected = finish
    assert expected == directive.tree
    assert ConversionType.OneToOne == directive.convert_type


def test_directive():
    orig = 'my input'
    output = 'my output'
    convert_type = ConversionType.PassThru
    directive = Directive(output, orig, convert_type)
    assert output == directive.tree
    assert orig == directive.orig_input
    assert convert_type == directive.convert_type


def test_di_locale():
    # FIXME needs .UTF-8 at the end in all cases?
    for locale in ['en_US', 'en_GB']:
        trivial(f'd-i debian-installer/locale string {locale}',
                {'locale': locale})


def test_di_locale_extra_stuff():
    locale = 'zz_ZZ'
    trivial(f' d-i debian-installer/locale string {locale} ',
            {'locale': locale})


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
        assert line == directive.orig_input
        assert ConversionType.PassThru == directive.convert_type


def test_di_keymap():
    # d-i keyboard-configuration/xkb-keymap select us
    # keyboard:
    #   layout: us
    for keymap in ['us', 'zz']:
        # breakpoint()
        trivial(f'd-i keyboard-configuration/xkb-keymap select {keymap}',
                {'keyboard': {'layout': keymap}})


def test_di_invalid():
    line = 'd-i stuff/things string asdf'
    directive = convert(line)
    assert {} == directive.tree
    assert ConversionType.UnknownError == directive.convert_type


def test_di_user_fullname():
    value = 'Debian User'
    # identity:
    #   realname: value
    trivial(f'd-i passwd/user-fullname string {value}',
            {'identity': {'realname': value}})


def test_di_username():
    value = 'debian'
    # username: value
    trivial(f'd-i passwd/username string {value}',
            {'identity': {'username': value}})


def test_di_user_password_crypted():
    value = '$6$wdAcoXrU039hKYPd$508Qvbe7ObUnxoj15DRCkzC3qO7edjH0VV7BPNRDYK4' \
            'QR8ofJaEEF2heacn0QgD.f8pO8SNp83XNdWG6tocBM1'
    # password: value
    trivial(f'd-i passwd/user-password-crypted string {value}',
            {'identity': {'password': value}})


def test_di_hostname():
    value = 'somehost'
    # hostname: value
    trivial(f'd-i netcfg/hostname string {value}',
            {'identity': {'hostname': value}})


# @pytest.mark.skip('convert to dict instead of line')
def test_di_ipaddress():
    value = '192.168.1.42'
    trivial(f'd-i netcfg/get_ipaddress string {value}',
            {'network': {'ethernets': {'any': {
                'match': {'name': 'en*'},
                'addresses': [value],
            }}}}) # FIXME merge with netmask


# @pytest.mark.skip('convert to dict instead of line')
def test_di_netmask():
    mask = '255.255.255.0'
    mask_bits = '24'
    trivial(f'd-i netcfg/get_netmask string {mask}',
            {'network': {'ethernets': {'any': {
                'match': {'name': 'en*'},
                'addresses': [mask_bits],
            }}}}) # FIXME merge with ipaddress
    # FIXME merge with ipaddress


def test_netmask_bits():
    table = {
            '255.255.255.0': '24',
            '255.255.0.0': '16',
    }
    for key in table:
        expected = table[key]
        assert expected == netmask_bits(key)


def test_di_gateway():
    value = '192.168.1.1'
    trivial(f'd-i netcfg/get_gateway string {value}',
            {'network': {'ethernets': {'any': {
                'match': {'name': 'en*'},
                'gateway4': value}}}})


# @pytest.mark.skip('convert to dict instead of line')
def test_di_nameservers():
    value = '192.168.1.1'
    trivial(f'd-i netcfg/get_nameservers string {value}',
            {'network': {'ethernets': {'any': {
                'match': {'name': 'en*'},
                'nameservers': {'addresses': [value]}}}}})


def test_insert_at_none():
    a = {'a': None}

    actual = insert_at_none(a, 1)
    expected = {'a': 1}
    assert expected == actual


def test_insert_at_none_second():
    b = {'a': {'b': None}}

    actual = insert_at_none(b, 1)
    expected = {'a': {'b': 1}}
    assert expected == actual


def test_insert_at_array():
    a = {'a': []}

    actual = insert_at_none(a, 1)
    expected = {'a': [1]}
    assert expected == actual
