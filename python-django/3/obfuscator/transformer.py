class Transformer:
    def __init__(self, techniques=None):
        self.techniques = techniques or []
    
    def transform(self, ast):
        current_ast = ast
        for technique in self.techniques:
            current_ast = technique.visit(current_ast)
            if current_ast is None:
                raise ValueError(f"Technique {technique.__class__.__name__} returned None")
        return current_ast
    
def apply_transformations(ast, techniques):
    transformer = Transformer(techniques)
    return transformer.transform(ast)