
from autoinstall_generator.convert import (convert, Directive, ConversionType,
                                           netmask_bits, insert_at_none)
from autoinstall_generator.merging import merge, bucketize
# import pytest


def full_flow(start, expected, convert_type):
    directives = []

    if type(start) == str:
        start = [start]

    for item in start:
        cur = convert(item)
        assert convert_type == cur.convert_type
        assert isinstance(cur.tree, dict)
        directives.append(cur)

    buckets = bucketize(directives)
    coalesced = buckets.coalesce()

    assert expected == merge(coalesced)


def one_to_one(start, expected):
    full_flow(start, expected, ConversionType.OneToOne)


def dependent(start, expected):
    full_flow(start, expected, ConversionType.Dependent)


def unsupported(start, expected):
    full_flow(start, expected, ConversionType.Unsupported)


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
        one_to_one(f'd-i debian-installer/locale string {locale}',
                   {'locale': locale})


def test_di_locale_extra_stuff():
    locale = 'zz_ZZ'
    one_to_one(f' d-i debian-installer/locale string {locale} ',
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
        one_to_one(f'd-i keyboard-configuration/xkb-keymap select {keymap}',
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
    one_to_one(f'd-i passwd/user-fullname string {value}',
               {'identity': {'realname': value}})


def test_di_username():
    value = 'debian'
    # username: value
    one_to_one(f'd-i passwd/username string {value}',
               {'identity': {'username': value}})


def test_di_user_password_crypted():
    value = '$6$wdAcoXrU039hKYPd$508Qvbe7ObUnxoj15DRCkzC3qO7edjH0VV7BPNRDYK4' \
            'QR8ofJaEEF2heacn0QgD.f8pO8SNp83XNdWG6tocBM1'
    # password: value
    one_to_one(f'd-i passwd/user-password-crypted string {value}',
               {'identity': {'password': value}})


def test_di_hostname():
    value = 'somehost'
    # hostname: value
    one_to_one(f'd-i netcfg/hostname string {value}',
               {'identity': {'hostname': value}})


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
    one_to_one(f'd-i netcfg/get_gateway string {value}',
               {'network': {'ethernets': {'any': {
                'match': {'name': 'en*'},
                'gateway4': value}}}})


def test_di_address_netmask():
    address = '192.168.1.42'
    mask = '255.255.255.0'
    mask_bits = '24'
    expected = {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'addresses': [f'{address}/{mask_bits}'],
    }}}}
    dependent([f'd-i netcfg/get_ipaddress string {address}',
               f'd-i netcfg/get_netmask string {mask}'],
              expected)


def test_di_mirror():
    # d-i mirror/http/hostname string http.us.debian.org
    # d-i mirror/http/directory string /debian
    hostname = 'http.us.debian.org'
    directory = '/debian'

    expected = {'apt': {
                   'primary': [{
                       'arches': ['default'],
                       'uri': f'http://{hostname}{directory}'}]}}
    dependent([f'd-i mirror/http/hostname string {hostname}',
               f'd-i mirror/http/directory string {directory}'],
              expected)


def test_dependent():
    value = 'asdf'
    for key in ['hostname', 'directory']:
        orig = f'd-i mirror/http/{key} string {value}'
        directive = convert(orig)

        assert ConversionType.Dependent == directive.convert_type
        assert orig == directive.orig_input
        assert {'mirror/http': {key: value}} == directive.fragments


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


def test_unsupported():
    lines = [
        'd-i localechooser/supported-locales multiselect en_US.UTF-8',
        'd-i debian-installer/language string en',
        'd-i debian-installer/country string NL',
        'd-i keyboard-configuration/toggle select No toggling',
    ]
    for line in lines:
        unsupported(line, {})


def test_duplicate():
    directives = []
    for locale in ['en_US', 'en_GB']:
        line = f'd-i debian-installer/locale string {locale}'
        directives.append(convert(line))
    actual = merge(directives)
    expected = {'locale': 'en_GB'}
    assert expected == actual


def test_directive_repr():
    dependent = Directive({}, 'netmask', ConversionType.Dependent)
    dependent.fragments = {'stuff': 'things'}
    onetoone = Directive({}, '1:1', ConversionType.OneToOne)
    onetoone.tree = {'first': {'second': 3}}
    directives = [
        (Directive({}, 'asdf', ConversionType.UnknownError),
         'UnknownError:"asdf"'),
        (Directive({}, 'pass', ConversionType.PassThru),
         'PassThru:"pass"'),
        (Directive({}, 'nope', ConversionType.Unsupported),
         'Unsupported:"nope"'),
        (dependent, f'Dependent:{dependent.fragments}'),
        (onetoone, f'OneToOne:{onetoone.tree}'),
    ]

    for d in directives:
        assert d[1] == repr(d[0])


def test_debug_directive():
    one = Directive({'stuff': 'things'}, 'my orig input',
                    ConversionType.OneToOne, 1)
    expected = '# 1: Directive: my orig input\n'
    actual, linenolen = one.debug_directive()
    assert expected == actual
    assert 1 == linenolen


# @pytest.mark.skip('debug overhaul')
def test_debug():
    one = Directive({'stuff': 'things'}, 'my orig input',
                    ConversionType.OneToOne, 1)
    expected = '''\
# 1: Directive: my orig input
#    Mapped to: stuff: things
'''
    assert expected == one.debug()


def test_debug_coallesce():
    coalesced = Directive({'a': 'b'}, 'asdf', ConversionType.Coalesced, 1)
    coalesced.children = [
            Directive({}, 'c', ConversionType.Dependent, 2),
            Directive({}, 'd', ConversionType.Dependent, 3),
    ]
    expected = '''\
# 2: Directive: c
# 3:       And: d
#    Mapped to: a: b
'''
    assert expected == coalesced.debug()


def test_debug_unsupported():
    unsupported = Directive({}, 'qwerty', ConversionType.Unsupported, 7)
    expected = '# 7: Unsupported: qwerty\n'
    assert expected == unsupported.debug_directive()[0]


def test_debug_error():
    error = Directive({}, 'oiqwueriower', ConversionType.UnknownError, 6)
    expected = '# 6: Error: oiqwueriower\n'
    assert expected == error.debug_directive()[0]
