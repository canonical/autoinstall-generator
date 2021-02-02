
def convert(line):
    tokens = line.split(' ')
    locale = tokens[3]
    return f'''Welcome:\n  lang: {locale}'''
