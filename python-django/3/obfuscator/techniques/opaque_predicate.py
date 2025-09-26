from abgoosht_parser.c_ast import NodeVisitor, Compound, If, Decl, Return, While, For, Switch, Break, Continue, BinaryOp, Constant

class OpaquePredicate(NodeVisitor):
    """
    Wraps simple statements inside an always-true 'if' condition (an opaque predicate).
    This excludes control flow statements and declarations.
    """
    def visit_Compound(self, node):
        if not node.block_items:
            return node

        new_items = []
        # Define the set of statement types that should NOT be wrapped.
        excluded_types = (If, Decl, Return, While, For, Switch, Break, Continue, Compound)

        for item in node.block_items:
            # Recursively visit the item first to process nested structures.
            visited_item = self.visit(item)

            if not isinstance(visited_item, excluded_types):
                # This is a simple statement that should be wrapped.
                
                # Create the always-true condition: 1 == 1
                opaque_cond = BinaryOp('==', Constant('int', '1'), Constant('int', '1'))
                
                # The body of the if is a new block containing the original statement.
                if_body = Compound([visited_item])
                
                # Create the new if statement.
                wrapped_item = If(cond=opaque_cond, iftrue=if_body, iffalse=None)
                new_items.append(wrapped_item)
            else:
                # This is an excluded type, so add it without modification.
                new_items.append(visited_item)
                
        node.block_items = new_items
        return node