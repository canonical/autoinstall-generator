
from convert import convert, Directive, ConversionType
import yaml


def do_merge(a, b):
    '''Take a pair of dictionaries, and provide the merged result.
       Assumes that any key conflicts have values that are themselves
       dictionaries and raises TypeError if found otherwise.'''
    result = a

    for key in b:
        if key in result:
            left = result[key]
            right = b[key]
            if type(left) is not dict or type(right) is not dict:
                raise TypeError('Only dictionaries can be merged')
            result[key] = do_merge(left, right)
        else:
            result[key] = b[key]

    return result


def merge(directives):
    '''Take a list of directives, and do_merge() their trees.'''

    result = {}
    for d in directives:
        result = do_merge(result, d.tree)

    return result


def coallesce(directives):
    '''Take a list of co-dependent directives, and output a coallesced
       Directive that represents resolution of all the dependent values.'''
    result = Directive({}, '', ConversionType.Coallesced)
    result.children = directives
    return result


def convert_file(filepath):
    directives = []

    with open(filepath, 'r') as preseed_file:
        for line in preseed_file.readlines():
            directive = convert(line)
            if directive.convert_type == ConversionType.OneToOne:
                directives.append(directive)

    result_dict = merge(directives)

    result = yaml.dump(result_dict, default_flow_style=False)

    return result
