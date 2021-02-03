
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
    line : str
        the output data generated from the orig_input line
    orig_input : str
        the input that was used to generate this Directive
    convert_type : ConversionType
        the type of conversion performed
    '''
    def __init__(self, line, orig_input, convert_type):
        self.line = line
        self.orig_input = orig_input
        self.convert_type = convert_type


conversion_table = {
    'keyboard-configuration/xkb-keymap': 'keyboard:\n  layout:',
    'debian-installer/locale': 'locale:',
    'passwd/user-fullname': 'identity:\n  realname:',
    'passwd/username': 'identity:\n  username:',
    'passwd/user-password-crypted': 'identity:\n  password:',
    'netcfg/hostname': 'identity:\n  hostname:',
}


def dispatch(key, value):
    output = ''

    if key in conversion_table:
        output = ' '.join((conversion_table[key], value))

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
        return Directive(line, line, ConversionType.PassThru)

    convert_type = ConversionType.OneToOne
    output = dispatch(tokens[1], ' '.join(tokens[3:]))

    if len(output) < 1:
        convert_type = ConversionType.UnknownError

    return Directive(output, line, convert_type)
