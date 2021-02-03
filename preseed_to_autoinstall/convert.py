
from enum import Enum


class ConversionType(Enum):
    UnknownError = 0,
    PassThru = 1,
    OneToOne = 2,


class Answer:
    '''
    A structure of values corresponding to how the conversion handled a given
    input line.

    Attributes
    ----------
    line : str
        the output data generated from the orig_input line
    orig_input : str
        the input that was used to generate this Answer
    convert_type : ConversionType
        the type of conversion performed
    '''
    def __init__(self, line, orig_input, convert_type):
        self.line = line
        self.orig_input = orig_input
        self.convert_type = convert_type


conversion_table = {
    'keyboard-configuration/xkb-keymap': 'Keyboard:\n  layout:',
    'debian-installer/locale': 'Welcome:\n  lang:',
    'passwd/user-fullname': 'Identity:\n  realname:',
    'passwd/username': 'Identity:\n  username:',
    'passwd/user-password-crypted': 'Identity:\n  password:',
    'netcfg/hostname': 'Identity:\n  hostname:',
}


def dispatch(key, value):
    output = ''

    if key in conversion_table:
        output = ' '.join((conversion_table[key], value))

    return output


def convert(line):
    '''Convert Debian install preseed line to Subiquity answer equivalent.

    Returns
    -------
    answer
        Answer object
    '''
    # assumptions:
    #  can process one line at a time
    #  whitespace-only lines and comments should pass thru

    trimmed = line.strip()
    tokens = trimmed.split(' ')
    if len(tokens) < 4 or tokens[0] != 'd-i':
        return Answer(line, line, ConversionType.PassThru)

    convert_type = ConversionType.OneToOne
    output = dispatch(tokens[1], ' '.join(tokens[3:]))

    if len(output) < 1:
        convert_type = ConversionType.UnknownError

    return Answer(output, line, convert_type)
