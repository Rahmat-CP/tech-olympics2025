from abgoosht_parser.c_ast import NodeVisitor, FuncDef, Compound, Decl, IdentifierType, TypeDecl, Constant, ID, Assignment, While, Switch, Case, Break, Return

class ControlFlowFlattener(NodeVisitor):
    """
    Rewrites the 'main' function's control flow using a state machine
    implemented with a while(1) loop and a switch-case statement.
    """
    def visit_FuncDef(self, node):
        # This transformation only applies to the 'main' function.
        if node.decl.name == 'main':
            if not node.body or not node.body.block_items:
                return node # Do nothing if main is empty.

            original_stmts = node.body.block_items
            new_body_stmts = []
            state_var_name = '__cf_state'
            
            # 1. Declare the state variable: 'int __cf_state = 0;'
            state_var_decl = Decl(
                name=state_var_name, quals=[], storage=[], funcspec=[],
                type=TypeDecl(declname=ID(name=state_var_name), quals=[], type=IdentifierType(['int'])),
                init=Constant('int', '0'), bitsize=None
            )
            new_body_stmts.append(state_var_decl)
            
            # 2. Build the list of cases for the switch statement.
            cases = []
            for i, stmt in enumerate(original_stmts):
                case_body = [stmt]
                # For any statement that is not a return, update the state and break.
                if not isinstance(stmt, Return):
                    state_update = Assignment(op='=', lvalue=ID(name=state_var_name), rvalue=Constant('int', str(i + 1)))
                    case_body.append(state_update)
                    case_body.append(Break())
                
                case_node = Case(expr=Constant('int', str(i)), stmts=case_body)
                cases.append(case_node)
            
            # 3. Create the switch statement.
            switch_stmt = Switch(cond=ID(name=state_var_name), stmt=Compound(block_items=cases))
            
            # 4. Create the 'while(1)' loop containing the switch.
            while_loop = While(cond=Constant('int', '1'), stmt=switch_stmt)
            new_body_stmts.append(while_loop)
            
            # 5. Replace the original function body with the new structure.
            node.body = Compound(block_items=new_body_stmts)

        return node