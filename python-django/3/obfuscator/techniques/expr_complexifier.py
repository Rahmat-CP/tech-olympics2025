from abgoosht_parser.c_ast import NodeVisitor, BinaryOp, Constant
import copy

class ExprComplexifier(NodeVisitor):
    """
    Replaces simple arithmetic expressions with more complex, equivalent forms.
    - 'a + b' is replaced with '(a ^ b) + ((a & b) << 1)'
    - 'a * 2' is replaced with 'a << 1'
    """
    def visit_BinaryOp(self, node):
        # First, recursively visit the left and right children of the operation.
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        # Handle the addition operator '+'
        if node.op == '+':
            # Create the expression: (left ^ right)
            xor_expr = BinaryOp('^', copy.deepcopy(node.left), copy.deepcopy(node.right))
            
            # Create the expression: (left & right)
            and_expr = BinaryOp('&', copy.deepcopy(node.left), copy.deepcopy(node.right))
            
            # Create the expression: ((left & right) << 1)
            shift_expr = BinaryOp('<<', and_expr, Constant('int', '1'))
            
            # Combine them: (a ^ b) + ((a & b) << 1)
            new_node = BinaryOp('+', xor_expr, shift_expr)
            return new_node
        
        # Handle the multiplication operator '*'
        elif node.op == '*':
            # Check for multiplication by 2.
            if isinstance(node.right, Constant) and node.right.value == '2':
                # Replace 'expr * 2' with 'expr << 1'
                new_node = BinaryOp('<<', node.left, Constant('int', '1'))
                return new_node
            elif isinstance(node.left, Constant) and node.left.value == '2':
                # Replace '2 * expr' with 'expr << 1'
                new_node = BinaryOp('<<', node.right, Constant('int', '1'))
                return new_node
        
        return node