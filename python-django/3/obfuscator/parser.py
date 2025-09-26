from abgoosht_parser import c_parser, c_ast

def parse_code(code):
    parser = c_parser.CParser()
    ast = parser.parse(code)
    return ast

def parse_file(filename):
    with open(filename, 'r') as f:
        code = f.read()
    return parse_code(code)