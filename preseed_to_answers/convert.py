
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


# assumptions:
#  can process one line at a time
#  whitespace-only lines and comments should pass thru


def convert(line):
    '''Convert Debian install preseed line to Subiquity answer equivalent.

    Returns
    -------
    answer
        Answer object
    '''
    trimmed = line.strip()
    tokens = trimmed.split(' ')
    if len(tokens) > 3 and tokens[0] == 'd-i':
        locale = tokens[3]
        output = f'''Welcome:\n  lang: {locale}'''
        return Answer(output, line, ConversionType.OneToOne)

    return Answer(line, line, ConversionType.PassThru)
