from abgoosht_parser.c_ast import NodeVisitor, Compound, If, For, Constant

class DeadCodeInserter(NodeVisitor):
    """
    Inserts dead code at the beginning and end of each non-empty code block.
    - Start of block: 'if (0) { 0; }'
    - End of block: 'for (;0;) { }'
    """
    def generic_visit(self, node):
        """
        Ensure all nodes are traversed and the node is returned.
        This handles visiting children of nodes like If, For, etc.,
        and makes sure we don't return None implicitly.
        """
        super().generic_visit(node)
        return node

    def visit_Compound(self, node):
        # First, recursively visit children to handle nested blocks correctly.
        if node.block_items:
            for i, item in enumerate(node.block_items):
                node.block_items[i] = self.visit(item)

        # Only add dead code to blocks that are not empty.
        if node.block_items:
            # Create a dead 'if' statement: if (0) { 0; }
            # Using Constant as a statement.
            dead_if_body = Compound(block_items=[Constant('int', '0')])
            dead_if = If(cond=Constant('int', '0'), iftrue=dead_if_body, iffalse=None)

            # Create a dead 'for' loop: for (; 0;) {}
            dead_for_body = Compound(block_items=[])
            dead_for = For(init=None, cond=Constant('int', '0'), next=None, stmt=dead_for_body)

            # Insert the dead code into the block.
            node.block_items.insert(0, dead_if)
            node.block_items.append(dead_for)
        
        return node

