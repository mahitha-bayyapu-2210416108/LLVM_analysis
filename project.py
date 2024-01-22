import re
import argparse
import os
from collections import OrderedDict

def parse_input(input_text):
    lines = input_text.strip().split('\n')
    if len(lines) > 0:
        function_declaration = lines[0].strip()
        function_name_match = re.search(r'define .*@(\w+)', function_declaration)
        function_name = function_name_match.group(1) if function_name_match else None
        instructions = [line.strip() for line in lines[1:]]
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

def analyze_flow(instructions):
    sources = set()
    sinks = set()
    relationships = []
    source = None

    for instruction in instructions:
        if 'call' in instruction and 'SOURCE' in instruction:
            source = re.findall(r'%\w+', instruction)[0]
            sources.add(source)
            relationships.append((source, None))
        if source is not None and 'store' in instruction and source in instruction:
            registers = re.findall(r'%\w+', instruction)

            if len(registers) == 2:   
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((registers[0], None))
                if source in sources:
                    sources.remove(source)
                    sources.add(registers[0])
            else:
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                if source in sources:
                    sources.remove(source)

        if source is not None and 'SOURCE' not in instruction and source in instruction:
            if 'load' in instruction:
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if source in relationships:
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                    
                if source in sources:
                    sources.remove(source)
                    sources.add(new_register)

            if 'add' in instruction and '0' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                                  
                if source in sources:
                    sources.remove(source)
                    sources.add(new_register)
            if 'sub' in instruction and '0' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                                  
                if source in sources:
                    sources.remove(source)
                    sources.add(new_register)
            if 'mul' in instruction and '1' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                                  
                if source in sources:
                    sources.remove(source)
                    sources.add(new_register)
            if 'div' in instruction and '1' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                   
                if source in sources:
                    sources.remove(source)
                    sources.add(new_register)

    for instruction in instructions:
        if 'call' in instruction and 'SINK' in instruction:
            sink = re.findall(r'%\w+', instruction)[0]
            sinks.add(sink)
            relationships.append((source, sink))
        for source in sources:
            if  source is not None and 'SOURCE' not in instruction and source in instruction and 'call' in instruction:
                fun = re.findall(r'%\w+', instruction)[0]
                sinks.add(fun)
                relationships.append((source, fun))
                
                '''
                %new_register_add = add i32 %res, 0
                %new_register_sub = sub i32 %res, 0
                %new_register_mul = mul i32 %res, 1
                %new_register_div = sdiv i32 %res, 1
                if these operations are performed, update source with a new register
                '''

    return sources, sinks, relationships

def detect_flow(instructions):
    sources, sinks, relationships = analyze_flow(instructions)
    for relationship in relationships:
        source, sink = relationship
        if source in sources and sink in sinks:
            print("LEAK")
            return

    print("NO LEAK")

parser = argparse.ArgumentParser(description='Generate graphviz dot files for LLVM functions.')
parser.add_argument('-i', '--infile', type=str, help='Input LLVM human-readable bitcode file (.ll)')
parser.add_argument('-o', '--outdir', type=str, help='Output directory for graphviz dot files')
parser.add_argument("-s", "--static", action="store_true", help='Perform flow analysis on LLVM code.')
args = parser.parse_args()

with open(args.infile, 'r') as file:
    llvm_code = file.read()

function_name, instructions = parse_input(llvm_code)

if args.outdir:
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
            dot_content = generate_dot_output(function_name, function_instructions, function_instructions_dict)
            
            with open(dot_file_path, 'w') as dot_file:
                print("digraph {", file=dot_file)
                print(dot_content, file=dot_file)
                print("}", file=dot_file)
            
            print(f"Done! {dot_file_path} generated.")
elif args.static:
    if function_name:
        detect_flow(instructions)
