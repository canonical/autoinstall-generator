
import copy
from enum import Enum
from merging import merge
import yaml


class ConversionType(Enum):
    UnknownError = 0,
    PassThru = 1,
    OneToOne = 2,


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
    '''
    def __init__(self, tree, orig_input, convert_type):
        self.tree = tree
        self.orig_input = orig_input
        self.convert_type = convert_type


def netmask_bits(value):
    # FIXME actually calculate it
    bits = '0'
    if value == '255.255.255.0':
        bits = '24'
    elif value == '255.255.0.0':
        bits = '16'
    return bits


def netmask(value):
    # FIXME dependency on ip address
    bits = netmask_bits(value)
    tree = {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'addresses': [],
    }}}}

    return insert_at_none(tree, bits)


# Translation table to map from preseed values to autoinstall ones.
# key: d-i style directive key
# value: dictionary for simple mapping, function for more exciting one
preseedmap = {
    'keyboard-configuration/xkb-keymap': {'keyboard': {'layout': None}},
    'debian-installer/locale': {'locale': None},
    'passwd/user-fullname': {'identity': {'realname': None}},
    'passwd/username': {'identity': {'username': None}},
    'passwd/user-password-crypted': {'identity': {'password': None}},
    'netcfg/hostname': {'identity': {'hostname': None}},
    'netcfg/get_netmask': netmask,
    'netcfg/get_gateway': {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'gateway4': None,
    }}}},
    'netcfg/get_nameservers': {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'nameservers': {'addresses': []},
    }}}},
    'netcfg/get_ipaddress': {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'addresses': [],
    }}}},
}


def dispatch(line, key, value):
    output = ''

    if key in preseedmap:
        mapped_key = preseedmap[key]
        if callable(mapped_key):
            output = mapped_key(value)
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


def convert_file(filepath):
    converted = []

    with open(filepath, 'r') as preseed_file:
        for line in preseed_file.readlines():
            directive = convert(line)
            if directive.convert_type == ConversionType.OneToOne:
                converted.append(directive)

    result_dict = {}
    while len(converted) > 0:
        cur = converted.pop()
        result_dict = merge(result_dict, cur.tree)

    result = yaml.dump(result_dict, default_flow_style=False)

    return result
