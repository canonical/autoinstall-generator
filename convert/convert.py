
# assumptions:
#  can process one line at a time

def convert(line):
    tokens = line.split(' ')
    if len(tokens) == 4:
        locale = tokens[3]
        return f'''Welcome:\n  lang: {locale}'''
    else:
        return line
