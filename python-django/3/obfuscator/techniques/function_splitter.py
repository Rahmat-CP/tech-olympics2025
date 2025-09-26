from abgoosht_parser.c_ast import NodeVisitor, FuncDef, TypeDecl, ID, ParamList, FuncCall, Return, Compound, Decl, FileAST
import copy

class _VariableUsageVisitor(NodeVisitor):
    """A helper visitor to find declared and used variables within a set of AST nodes."""
    def __init__(self):
        self.declared_vars = set()
        self.used_vars = set()

    def visit_Decl(self, node):
        if node.name:
            self.declared_vars.add(node.name)
        # Also visit the initializer part of the declaration for used variables
        if node.init:
            self.visit(node.init)

    def visit_ID(self, node):
        self.used_vars.add(node.name)

class FunctionSplitter(NodeVisitor):
    """
    Splits any function with more than two statements into two parts.
    The second part becomes a new helper function, which is called by the first.
    """
    def __init__(self):
        self.split_func_counter = 0
        self.new_funcs = []

    def visit_FileAST(self, node):
        # We need to collect new functions and add them at the end.
        self.new_funcs = []
        # First, traverse the existing functions. self.visit_FuncDef will be called.
        self.generic_visit(node)
        # Add the newly created split functions to the AST.
        node.ext.extend(self.new_funcs)
        return node

    def visit_FuncDef(self, node):
        # Process the body of the function first
        if node.body:
            self.visit(node.body)

        if node.body and node.body.block_items and len(node.body.block_items) > 2:
            # 1. Find the split point (middle of the function body).
            statements = node.body.block_items
            split_idx = len(statements) // 2
            first_half_stmts = statements[:split_idx]
            second_half_stmts = statements[split_idx:]

            # 2. Analyze variable usage.
            first_half_visitor = _VariableUsageVisitor()
            for stmt in first_half_stmts:
                first_half_visitor.visit(stmt)
            
            second_half_visitor = _VariableUsageVisitor()
            for stmt in second_half_stmts:
                second_half_visitor.visit(stmt)

            original_params = {p.name for p in (node.decl.type.args.params or []) if hasattr(p, 'name')}
            vars_to_pass_names = (first_half_visitor.declared_vars | original_params) & second_half_visitor.used_vars
            
            # 3. Create the new helper function.
            new_func_name = f"{node.decl.name}_split_{self.split_func_counter}"
            self.split_func_counter += 1

            # Build a map of variable names to their declarations for the new function's signature
            param_decl_map = {p.name: p for p in (node.decl.type.args.params or [])}
            class DeclFinder(NodeVisitor):
                def visit_Decl(self, n):
                    if n.name in vars_to_pass_names and n.name not in param_decl_map:
                        # Parameters are also Decl nodes.
                        param_decl_map[n.name] = Decl(
                            name=n.name, quals=[], storage=[], funcspec=[], 
                            type=copy.deepcopy(n.type), init=None, bitsize=None
                        )
            DeclFinder().visit(Compound(block_items=first_half_stmts))

            new_func_params = [param_decl_map[name] for name in sorted(list(vars_to_pass_names)) if name in param_decl_map]

            new_func_decl_type = copy.deepcopy(node.decl.type)
            new_func_decl_type.args = ParamList(new_func_params)
            new_func_decl = Decl(name=new_func_name, type=new_func_decl_type, quals=[], storage=[], funcspec=[])

            new_func = FuncDef(decl=new_func_decl, param_decls=None, body=Compound(block_items=second_half_stmts))
            self.new_funcs.append(new_func)
            
            # 4. Modify the original function to call the new helper function.
            call_args = [ID(name) for name in sorted(list(vars_to_pass_names))]
            func_call = FuncCall(name=ID(new_func_name), args=call_args)
            
            is_void = isinstance(node.decl.type.type, TypeDecl) and \
                      hasattr(node.decl.type.type.type, 'names') and \
                      'void' in node.decl.type.type.type.names

            last_stmt = func_call if is_void else Return(expr=func_call)

            node.body.block_items = first_half_stmts + [last_stmt]
        return node

