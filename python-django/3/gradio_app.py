import gradio as gr
import os
import time
import tempfile
from datetime import datetime
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

import subprocess

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BENCHMARK_DIR = os.path.join(BASE_DIR, "benchmarks")
os.makedirs(BENCHMARK_DIR, exist_ok=True)

def run_code(code):
    with tempfile.NamedTemporaryFile(suffix=".c", delete=False, mode="w", encoding="utf-8") as c_file:
        temp_c = c_file.name
        c_file.write(f"#include <stdio.h>\n#include <stdlib.h>\n\n{code}")

    temp_bin = temp_c + ".out"
    try:
        compile_result = subprocess.run(["gcc", temp_c, "-o", temp_bin], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return f"Compilation failed.\n{e.stderr}", 0.0, False

    start = time.time()
    try:
        run_result = subprocess.run([temp_bin], capture_output=True, text=True, check=True, timeout=5)
        output = run_result.stdout
        success = True
    except subprocess.CalledProcessError as e:
        output = e.stdout + e.stderr
        success = False
    except subprocess.TimeoutExpired:
        return "Execution timed out.", 5.0, False
    end = time.time()

    os.remove(temp_c)
    os.remove(temp_bin)
    return output, end - start, success

def get_stats(code):
    lines = code.count('\n') + 1
    chars = len(code)
    size = len(code.encode("utf-8"))
    return lines, chars, size

def benchmark_files(original_code, obfuscated_code):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    benchmark_path = os.path.join(BENCHMARK_DIR, f"{timestamp}_benchmark.txt")

    orig_out, orig_time, _ = run_code(original_code)
    obf_out, obf_time, _ = run_code(obfuscated_code)

    orig_stats = get_stats(original_code)
    obf_stats = get_stats(obfuscated_code)

    same_output = orig_out.strip() == obf_out.strip()

    # FIX: Added encoding='utf-8' and replaced emoji with text.
    with open(benchmark_path, "w", encoding="utf-8") as f:
        f.write(f"# Benchmark: {timestamp}\n")
        f.write(f"Functional Equivalence: {'Yes' if same_output else 'No'}\n\n")
        f.write("Original Code Stats:\n")
        f.write(f"   Lines     : {orig_stats[0]}\n")
        f.write(f"   Characters: {orig_stats[1]}\n")
        f.write(f"   File Size : {orig_stats[2]} bytes\n")
        f.write(f"   Run Time  : {orig_time:.4f} sec\n\n")
        f.write("Obfuscated Code Stats:\n")
        f.write(f"   Lines     : {obf_stats[0]}\n")
        f.write(f"   Characters: {obf_stats[1]}\n")
        f.write(f"   File Size : {obf_stats[2]} bytes\n")
        f.write(f"   Run Time  : {obf_time:.4f} sec\n\n")
        if not same_output:
            f.write("Outputs differ.\n")

    return f"""
### Functional Equivalence: {'Yes' if same_output else 'No'}

#### Original Code
- Lines: {orig_stats[0]}
- Characters: {orig_stats[1]}
- Size: {orig_stats[2]} bytes
- Runtime: {orig_time:.4f} sec
- Code output: 
```
{orig_out}
```

#### Obfuscated Code
- Lines: {obf_stats[0]}
- Characters: {obf_stats[1]}
- Size: {obf_stats[2]} bytes
- Runtime: {obf_time:.4f} sec
- Code output:
```
{obf_out}
```

Benchmark saved to: `{benchmark_path}`
"""

def process_code(code, obf_techniques):
    ast = parse_code(code)
    if not ast:
        return "Parsing failed.", ""

    technique_map = {
        "VariableRenamer": VariableRenamer(),
        "DeadCodeInserter": DeadCodeInserter(),
        "MisleadingComments": MisleadingComments(),
        "FunctionSplitter": FunctionSplitter(),
        "ExprComplexifier": ExprComplexifier(),
        "AliasGenerator": AliasGenerator(),
        "OpaquePredicate": OpaquePredicate(),
        "ControlFlowFlattener": ControlFlowFlattener(),
    }
    chosen = [technique_map[name] for name in obf_techniques if name in technique_map]

    transformer = Transformer(chosen)
    transformed_ast = transformer.transform(ast)
    result_code = generate_code(transformed_ast)

    benchmark_result = benchmark_files(code, result_code)
    return result_code, benchmark_result


with gr.Blocks(title="MiniC Obfuscator") as demo:
    gr.Markdown("# 🍲 Abgoosht: MiniC Code Obfuscator")
    gr.Markdown("Choose your techniques, and benchmark the result.")

    code_input = gr.Code(label="Input MiniC Code", language="c", value="""
int main(){
    printf("Hello world");
    return 0;
}
""")

    with gr.Accordion("🔧 Techniques", open=True):
        obf_techniques = gr.CheckboxGroup(
            choices=[
                "VariableRenamer", "DeadCodeInserter", "MisleadingComments",
                "FunctionSplitter", "ExprComplexifier", "AliasGenerator", "OpaquePredicate", "ControlFlowFlattener"
            ],
            label="Obfuscation Techniques",
            value=["VariableRenamer", "DeadCodeInserter"]
        )

    run_btn = gr.Button("🚀 Run")

    with gr.Row():
        code_output = gr.Code(label="🧠 Resulting Code", language="c")
        benchmarks = gr.Markdown(label="📈 Benchmark Results")

    run_btn.click(fn=process_code,
                  inputs=[code_input, obf_techniques],
                  outputs=[code_output, benchmarks])

demo.launch(server_name="0.0.0.0", server_port=80)

