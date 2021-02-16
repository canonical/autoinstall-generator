
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


def merge(dicts):
    '''Take a list of dictionaries, and do_merge() them all.'''

    result = {}
    for d in dicts:
        result = do_merge(result, d)

    return result
