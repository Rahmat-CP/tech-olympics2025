import argparse

from obfuscator.parser import parse_code
from obfuscator.transformer import Transformer
from obfuscator.generators import generate_code

from obfuscator.techniques.rename_vars import VariableRenamer
from obfuscator.techniques.dead_code import DeadCodeInserter
from obfuscator.techniques.misleading_comments import MisleadingComments
from obfuscator.techniques.function_splitter import FunctionSplitter
from obfuscator.techniques.expr_complexifier import ExprComplexifier
from obfuscator.techniques.alias_generator import AliasGenerator

from obfuscator.techniques.opaque_predicate import OpaquePredicate
from obfuscator.techniques.flow_flattener import ControlFlowFlattener

OBF_TECHNIQUES = {
    'rename_vars': VariableRenamer,
    'dead_code': DeadCodeInserter,
    'misleading_comments': MisleadingComments,
    'expr_complexifier': ExprComplexifier,
    'alias_generator': AliasGenerator,
    'function_splitter': FunctionSplitter,
    'opaque_predicate': OpaquePredicate,
    'flow_flattener': ControlFlowFlattener,
}

def parse_techniques(arg_value, available):
    selected = [name.strip() for name in arg_value.split(',')]
    techniques = []
    for name in selected:
        if name not in available:
            raise ValueError(f"Unknown technique: {name}")
        inst = available[name]()
        techniques.append(inst)
    return techniques

def main():
    parser = argparse.ArgumentParser(description='MiniC Obfuscation Tool')
    
    parser.add_argument('-i', '--input', help='Input MiniC file', default='input.mc')
    parser.add_argument('-o', '--output', help='Output file', default='output.mc')
    parser.add_argument('--obf', action='store_true', help='Apply obfuscation')
    parser.add_argument('--obf-techs', help='Comma-separated list of obfuscation techniques')

    args = parser.parse_args()

    try:
        with open(args.input, 'r') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return

    ast = parse_code(code)
    if ast is None:
        print("Error: Failed to parse AST")
        return

    try:
        if args.obf:
            techniques = parse_techniques(args.obf_techs, OBF_TECHNIQUES) if args.obf_techs else [fn() for fn in OBF_TECHNIQUES.values()]
        else:
            print("Please specify --obf or --deobf, or --benchmark")
            return

        transformer = Transformer(techniques=techniques)
        result_ast = transformer.transform(ast) or ast
    except Exception as e:
        print(f"Transformation failed: {str(e)}")
        return

    output_code = generate_code(result_ast)
    if not output_code:
        print("Code generation failed")
        return

    try:
        with open(args.output, 'w') as f:
            f.write(output_code)
        print(f"Successfully wrote to {args.output}")
    except Exception as e:
        print(f"Error writing output: {str(e)}")

if __name__ == "__main__":
    main()
