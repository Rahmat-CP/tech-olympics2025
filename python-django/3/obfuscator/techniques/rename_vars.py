import random
import string
from abgoosht_parser.c_ast import NodeVisitor, FuncDef, Decl, ID, TypeDecl

class VariableRenamer(NodeVisitor):
    """
    Renames all local variables and function parameters to random 8-character strings.
    A new renaming scope is created for each function.
    """

    def generic_visit(self, node):
        """
        Override generic_visit to ensure the node is returned after visiting children.
        The default visitor can return None, which causes an error in the transformer.
        """
        super().generic_visit(node)
        return node

    def visit_FuncDef(self, node):
        # Create a new renamer instance for each function to handle scope properly.
        func_renamer = _FunctionScopeRenamer()
        func_renamer.visit(node)
        return node

class _FunctionScopeRenamer(NodeVisitor):
    """
    Handles the renaming logic for a single function's scope.
    """
    def __init__(self):
        # Maps old_name -> new_name for the current function scope.
        self.name_map = {}
        self.used_names = set()

    def _generate_new_name(self):
        # Generates a unique random 8-character name.
        chars = string.ascii_letters
        while True:
            name = ''.join(random.choice(chars) for _ in range(8))
            if name not in self.used_names:
                self.used_names.add(name)
                return name

    def generic_visit(self, node):
        """
        Ensure all nodes are traversed and returned correctly.
        """
        super().generic_visit(node)
        return node

    def visit_FuncDef(self, node):
        # First, handle the parameters of the function.
        if node.decl.type.args:
            for param in node.decl.type.args.params:
                # Parameters are represented as Decl nodes.
                if isinstance(param, Decl) and param.name:
                    new_name = self._generate_new_name()
                    self.name_map[param.name] = new_name
                    param.name = new_name
        # Then, visit the body of the function to rename local variables and usages.
        if node.body:
            self.visit(node.body)
        return node

    def visit_Decl(self, node):
        # Rename any variable usages in the initializer expression first.
        if node.init:
            self.visit(node.init)
        
        # Now, rename the variable being declared, if it has a name.
        if node.name:
            if node.name not in self.name_map:
                new_name = self._generate_new_name()
                self.name_map[node.name] = new_name
            node.name = self.name_map[node.name]
        
        # Also visit the type declaration in case of complex types
        if node.type:
            self.visit(node.type)

        return node
    
    def visit_ID(self, node):
        # Rename a variable usage (ID) if it's in our scope map.
        if node.name in self.name_map:
            node.name = self.name_map[node.name]
        return node
    
    def visit_TypeDecl(self, node):
        # This handles renaming the declname inside a TypeDecl.
        if hasattr(node, 'declname') and node.declname in self.name_map:
            node.declname = self.name_map[node.declname]
        return node

