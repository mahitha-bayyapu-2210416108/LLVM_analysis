import re
import argparse

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
                sources.remove(source)
                sources.add(registers[0])
            else:
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                sources.remove(source)

        if source is not None and 'SOURCE' not in instruction and source in instruction:
            
            if 'load' in instruction:
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                   
                
                sources.remove(source)
                sources.add(new_register)
            if 'add' in instruction and '0' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                   
                
                sources.remove(source)
                sources.add(new_register)
            if 'sub' in instruction and '0' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                   
                
                sources.remove(source)
                sources.add(new_register)
            if 'mul' in instruction and '1' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                   
                
                sources.remove(source)
                sources.add(new_register)
            if 'div' in instruction and '1' in instruction.split(' '):
                new_register = re.findall(r'%\w+', instruction)[0]
                
                if any(source in rel[0] for rel in relationships):
                    relationships.remove((source, None))
                    relationships.append((new_register, None))
                   
                
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

parser = argparse.ArgumentParser(description='Perform flow analysis on LLVM code.')
parser.add_argument('-i', '--infile', type=str, help='Input LLVM human-readable bitcode file (.ll)')
args = parser.parse_args()

with open(args.infile, 'r') as file:
    llvm_ir_code = file.read()

function_name, instructions = parse_input(llvm_ir_code)

if function_name:
    detect_flow(instructions)
