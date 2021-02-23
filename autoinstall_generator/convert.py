
import copy
from enum import Enum


class ConversionType(Enum):
    # generic error
    UnknownError = 0
    # input lines that get passed thru - comments and what not
    PassThru = 1
    # a single d-i directive that has a 1:1 mapping with an autoinstall
    OneToOne = 2
    # a d-i directive that, when paired with matching Dependent
    # directives, can output autoinstall directive(s)
    Dependent = 3
    # the result of two or more Dependent directives being grouped into
    # a single, resolved, directive
    Coalesced = 4
    # a d-i directive that is recognized as being relevant to the
    # installer, but does not yet have a supported autoinstaller
    # mapping.
    Unsupported = 5


class Directive:
    '''
    A structure of values corresponding to how the conversion handled a given
    input line.

    Attributes
    ----------
    tree : dict
        the output data generated from the orig_input line in the form
        of a hierarchy of dictionaries
    orig_input : str
        the input that was used to generate this Directive
    convert_type : ConversionType
        the type of conversion performed
    fragments : dict
        partial data derived from Dependent preseed directives that,
        when coallased with all other Dependent directives, will yield a
        useable output
    children : list of Directive
        a list of child Directive objects that were the source of this
        Directive
    '''
    def __init__(self, tree, orig_input, convert_type):
        self.tree = tree
        self.orig_input = orig_input
        self.convert_type = convert_type
        self.fragments = {}
        self.children = []


def netmask_bits(value):
    # FIXME actually calculate it
    bits = '0'
    if value == '255.255.255.0':
        bits = '24'
    elif value == '255.255.0.0':
        bits = '16'
    return bits


def netmask(value, line):
    bits = netmask_bits(value)
    directive = Directive({}, line, ConversionType.Dependent)
    directive.fragments = {'netcfg': {'netmask_bits': bits}}
    return directive


def ipaddress(value, line):
    directive = Directive({}, line, ConversionType.Dependent)
    directive.fragments = {'netcfg': {'ipaddress': value}}
    return directive


def mirror_http_hostname(value, line):
    directive = Directive({}, line, ConversionType.Dependent)
    directive.fragments = {'mirror/http': {'hostname': value}}
    return directive


def mirror_http_directory(value, line):
    directive = Directive({}, line, ConversionType.Dependent)
    directive.fragments = {'mirror/http': {'directory': value}}
    return directive


# Translation table to map from preseed values to autoinstall ones.
# key: d-i style directive key
# value: dictionary for simple mapping, function for more exciting one,
#        None if unsupported
preseed_map = {
    'keyboard-configuration/xkb-keymap': {'keyboard': {'layout': None}},
    'debian-installer/locale': {'locale': None},
    'passwd/user-fullname': {'identity': {'realname': None}},
    'passwd/username': {'identity': {'username': None}},
    'passwd/user-password-crypted': {'identity': {'password': None}},
    'netcfg/hostname': {'identity': {'hostname': None}},
    'netcfg/get_gateway': {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'gateway4': None,
    }}}},
    'netcfg/get_nameservers': {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'nameservers': {'addresses': []},
    }}}},
    'netcfg/get_netmask': netmask,
    'netcfg/get_ipaddress': ipaddress,
    'mirror/http/hostname': mirror_http_hostname,
    'mirror/http/directory': mirror_http_directory,
    'localechooser/supported-locales': None,
    'debian-installer/language': None,
    'debian-installer/country': None,
}


def dispatch(line, key, value):
    output = {}

    if key in preseed_map:
        mapped_key = preseed_map[key]
        if not mapped_key:
            return Directive({}, line, ConversionType.Unsupported)
        elif callable(mapped_key):
            return mapped_key(value, line)
        else:
            output = insert_at_none(copy.deepcopy(mapped_key), value)

    convert_type = ConversionType.OneToOne
    if len(output) < 1:
        convert_type = ConversionType.UnknownError
        output = {}

    return Directive(output, line, convert_type)


def convert(line):
    '''Convert Debian install preseed line to Subiquity directive equivalent.

    Returns
    -------
    directive
        Directive object
    '''
    # assumptions:
    #  can process one line at a time
    #  whitespace-only lines and comments should pass thru

    trimmed = line.strip()
    tokens = trimmed.split(' ')
    if tokens[0] != 'd-i':
        return Directive({}, line, ConversionType.PassThru)

    value = ''
    if len(tokens) > 3:
        value = ' '.join(tokens[3:])

    return dispatch(line, tokens[1], value)


def insert_at_none(tree, value):
    '''Walk tree looking for None or empty array, then insert value.'''
    for key in tree:
        cur = tree[key]
        if type(cur) is dict:
            tree[key] = insert_at_none(cur, value)
        elif type(cur) is list and len(cur) == 0:
            tree[key] = [value]
        elif cur is None:
            tree[key] = value
    return tree
