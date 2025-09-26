from abgoosht_parser.c_ast import NodeVisitor, Decl, ID
import copy

class AliasGenerator(NodeVisitor):
    """
    Creates an alias for each variable declared within a function body.
    For a declaration like 'int a = 10;', it adds 'int a_alias = a;'.
    """
    def visit_Compound(self, node):
        # A Compound node represents a block of code, e.g., { ... }
        if not node.block_items:
            return node

        # We build a new list of statements to avoid modifying the list while iterating.
        new_items = []
        for item in node.block_items:
            # Add the original statement first.
            new_items.append(item)
            
            # Check if the statement is a variable declaration.
            if isinstance(item, Decl) and isinstance(item.type, (
                # We target simple type declarations, not function or array declarations in this context.
                # Assuming the c_ast structure has TypeDecl for simple types.
                __import__('abgoosht_parser.c_ast').c_ast.TypeDecl
            )):
                # Define the alias variable name.
                alias_name = item.name + '_alias'
                
                # Create the new declaration for the alias.
                # It has the same type as the original variable.
                # Its initial value is the original variable itself.
                alias_decl = Decl(
                    name=alias_name,
                    quals=item.quals[:],
                    storage=item.storage[:],
                    funcspec=item.funcspec[:],
                    type=copy.deepcopy(item.type),
                    init=ID(name=item.name), # e.g., init = a
                    bitsize=None,
                    coord=item.coord
                )
                
                # Add the new alias declaration to our list of statements.
                new_items.append(alias_decl)
        
        # Replace the old list of statements with our new, modified list.
        node.block_items = new_items
        return node

    def visit_FuncDef(self, node):
        # Start the process by visiting the body of each function definition.
        if node.body:
            self.visit(node.body)
        return node