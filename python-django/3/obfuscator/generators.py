from abgoosht_parser.c_generator import CGenerator

class CustomGenerator(CGenerator):
    def __init__(self):
        super().__init__()
        self.indent_level = 0

def generate_code(ast):
    generator = CustomGenerator()
    return generator.visit(ast)