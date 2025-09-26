from abgoosht_parser.c_ast import NodeVisitor, Compound

# This technique assumes that the parser and generator support a 'Comment' node.
# If not, this class would need to be created or an alternative like '#pragma' used.
try:
    from abgoosht_parser.c_ast import Comment
except ImportError:
    # Define a dummy Comment class if it doesn't exist in the provided AST.
    class Comment:
        def __init__(self, text, coord=None):
            self.text = text
            self.coord = coord

class MisleadingComments(NodeVisitor):
    """
    Adds a misleading comment to the beginning of each non-empty code block,
    cycling through a predefined list of comments.
    """
    def __init__(self):
        self.counter = 0
        self.comments = [
            "// optimization level={};",
            "// todo: refactor this loop;",
            "// warning: potential overflow at line {};",
            "// debug: value of x is unknown;",
            "// temporary hack, remove later;",
        ]

    def visit_Compound(self, node):
        # Recursively visit children first.
        if node.block_items:
            for i, item in enumerate(node.block_items):
                node.block_items[i] = self.visit(item)

        if node.block_items:
            # Select and format the next comment in the cycle.
            comment_template = self.comments[self.counter % len(self.comments)]
            comment_text = comment_template.format(self.counter)
            
            # Create a comment node.
            comment_node = Comment(text=comment_text)

            # Insert the comment at the beginning of the block.
            node.block_items.insert(0, comment_node)
            
            self.counter += 1

        return node