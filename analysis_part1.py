import re
import argparse
import os
from collections import OrderedDict

def parse_input(input_text):
    lines = input_text.strip().split('\n')
    if len(lines) > 0:
        function_declaration = lines[0].strip()
        function_name_match = re.search(r'@(\w+)', function_declaration)
        function_name = function_name_match.group(1) if function_name_match else None
        instructions = [line.strip() for line in lines[1:-1]]
        return function_name, instructions
    else:
        return None, None

def find_instruction(label, instructions):
    for instruction in instructions:
        if f"{label}:" in instruction:
            return instruction
    return None

def find_function(label, instructions):
    for instruction in instructions:
        if f"{label}(" in instruction:
            return instruction
    return None

def generate_dot_output(function_name, instructions, instructions_dict):
    dot_content = ""
    matches_dict = OrderedDict()
    i = 0  # Initialize the basic block index

    for block_name, basic_block in instructions_dict.items():
        dot_content += f'\t Node{i} [shape=record,label=""]\n'
        print("blocks:", block_name)
        for instruction in basic_block:
            if 'br ' in instruction:
                pattern = r"label %(\w+)"
                matches = re.findall(pattern, instruction)
                k = 1

                for match in matches:
                    matches_dict[match] = None
                    associated_instruction = find_instruction(match, instructions)

                    if associated_instruction:
                        unique_matches_list = list(matches_dict.keys())
                        index = unique_matches_list.index(match)
                        dot_content += f"\t Node{i} -> Node{index+1} [label={k}];\n"
                        k += 1
            elif 'call ' in instruction:
                pattern = r"@(\w+)"
                matches = re.findall(pattern, instruction)
                k = 1

                for match in matches:
                    matches_dict[match] = None
                    associated_instruction = find_function(match, instructions)

                    if associated_instruction:
                        unique_matches_list = list(matches_dict.keys())
                        index = unique_matches_list.index(match)
                        dot_content += f"\t Node{i} -> Node{index+1} [label={k}];\n"
                        k += 1
        i += 1

    return dot_content

parser = argparse.ArgumentParser(description='Generate graphviz dot files for LLVM functions.')
parser.add_argument('-i', '--infile', type=str, help='Input LLVM human-readable bitcode file (.ll)')
parser.add_argument('-o', '--outdir', type=str, help='Output directory for graphviz dot files')
args = parser.parse_args()

with open(args.infile, 'r') as file:
    llvm_code = file.read()

functions = re.findall(r'define \w+ @(\w+)', llvm_code)

os.makedirs(args.outdir, exist_ok=True)  # Create output directory if it doesn't exist

for function_name in functions:
    function_code = re.search(r'define \w+ @{}(.+?)[\n\s]*}}'.format(function_name), llvm_code, re.DOTALL)

    if function_code:
        function_code = function_code.group(0)
        function_instructions = function_code.strip().split('\n')[1:-1]
        dot_file_path = f'{args.outdir}/{function_name}.dot'
        print(f"Generating {dot_file_path}")
        
        # Organize instructions into basic blocks
        block_names = f"{function_name}"
        function_instructions_dict = {block_names: []}
        
        for instruction in function_instructions:
            if ':' in instruction:
                block_names = f"{instruction.strip(':')}"
                function_instructions_dict[block_names] = []
            else:
                function_instructions_dict[block_names].append(instruction)
        print("fun inst dic:", function_instructions_dict)
        dot_content = generate_dot_output(function_name, function_instructions, function_instructions_dict)
        
        with open(dot_file_path, 'w') as dot_file:
            print("digraph {", file=dot_file)
            print(dot_content, file=dot_file)
            print("}", file=dot_file)
        
        print(f"Done! {dot_file_path} generated.")
