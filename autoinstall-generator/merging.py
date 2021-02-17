
from convert import convert, Directive, ConversionType
import copy
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


def coalesce(directives):
    '''Take a list of co-dependent directives, and output a coalesced
       Directive that represents resolution of all the dependent values.'''
    result = Directive({}, '', ConversionType.Coalesced)
    result.children = directives

    result.fragments = {}
    for d in directives:
        result.fragments = do_merge(result.fragments, d.fragments)

    hostname = result.fragments['mirror/http']['hostname']
    directory = result.fragments['mirror/http']['directory']
    result.tree = {
        'apt': {
            'primary': [
                {
                    'arches': ['default'],
                    'uri': f'http://{hostname}{directory}'
                }
            ]
        }
    }

    return result


class Bucket:
    def __init__(self):
        self.independent = []
        self.dependent = {}
    def coalesce(self):
        result = copy.copy(self.independent)
        for key in self.dependent:
            cur = self.dependent[key]
            result.append(coalesce(cur))
        return result


def bucketize(directives):
    '''Categorize Directives into independent and dependent.  Dependent
       type directives are grouped into a list in the dependent dict and
       grouped on their fragment toplevel key.  Non-Dependent type
       directives are placed into the independent list.'''

    bucket = Bucket()

    for cur in directives:
        if cur.convert_type != ConversionType.Dependent:
            bucket.independent.append(cur)
            continue

        key = list(cur.fragments)[0]
        if key not in bucket.dependent:
            bucket.dependent[key] = [cur]
        else:
            bucket.dependent[key].append(cur)

    return bucket


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
