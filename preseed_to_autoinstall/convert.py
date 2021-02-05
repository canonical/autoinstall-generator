
import copy
from enum import Enum


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


# def netmask(value):
#     bits = netmask_bits(value)

#     # FIXME dependency on ip address
#     # FIXME dashed format
#     return {
#         'network': {
#             'ethernets': {
#                 'any': {
#                     'match': {'name': 'en*'},
#                     'addresses': bits,
#                 }
#             }
#         }
#     }


def nameservers(value):
    return f'''network:
  ethernets:
    any:
      match:
        name: en*'
      nameservers:
        addresses: [{value}]'''


# values that have a straightforward mapping can be just sent along
preseedmap = {
    'keyboard-configuration/xkb-keymap': {'keyboard': {'layout': None}},
    'debian-installer/locale': {'locale': None},
    'passwd/user-fullname': {'identity': {'realname': None}},
    'passwd/username': {'identity': {'username': None}},
    'passwd/user-password-crypted': {'identity': {'password': None}},
    'netcfg/hostname': {'identity': {'hostname': None}},
    # 'netcfg/get_netmask': netmask,
    'netcfg/get_gateway': {'network': {'ethernets': {'any': {
        'match': {'name': 'en*'},
        'gateway4': None,
    }}}},
    # 'netcfg/get_nameservers': nameservers,
    # 'netcfg/get_ipaddress': '''network:
    # ethernets:
    #   any:
    #     match:
    #       name: en*'
    #     addresses:
    #       -''',
}


def dispatch(key, value):
    output = ''

    if key in preseedmap:
        mapped_key = preseedmap[key]
        if callable(mapped_key):
            output = mapped_key(value)
        else:
            output = copy.deepcopy(mapped_key)
            output = insert_at_none(output, value)

    return output


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
    if len(tokens) < 4 or tokens[0] != 'd-i':
        return Directive({}, line, ConversionType.PassThru)

    convert_type = ConversionType.OneToOne
    output = dispatch(tokens[1], ' '.join(tokens[3:]))

    if len(output) < 1:
        convert_type = ConversionType.UnknownError
        output = {}

    return Directive(output, line, convert_type)


def insert_at_none(tree, value):
    for key in tree:
        cur = tree[key]
        if type(cur) is dict:
            tree[key] = insert_at_none(cur, value)
        elif cur is None:
            tree[key] = value
            break
    return tree
