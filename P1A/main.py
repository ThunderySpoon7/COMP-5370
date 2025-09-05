import sys, re
from urllib.parse import unquote

LOWER_ALPHA = [chr(i) for i in range(0x61, 0x7b)]
BEGIN_MAP = "(<"
END_MAP = ">)"

def error(msg:str):
    print(f"ERROR -- {msg}", file=sys.stderr)
    exit(66)

# Parses and removes key and ':' from inp
# returns key, modified inp
def parse_key(inp:str) -> tuple[str, str]:
    try:
        key_len = inp.index(':')
    except ValueError:
        error("Expected ':' separating key and value")
    
    key = inp[:key_len]
    if not (key.islower() and key.isalpha()):
            error(f"Keys must be lowercase alpha strings. Found key: '{key}'")

    print(f"{key} -- ", end="")
    return key, inp[key_len+1:]

def decode_num(value:str) -> str:
    try:
        return str(int(value, 2) - ((1 << len(value)) if value[0] == "1" else 0))
    except ValueError:
        error("Type num value must be expressed in two's complement binary and must not exceed 14,279 bits")

def decode_simple(value:str) -> str:
    return value[:-1]

def decode_complex(value:str) -> str:
    return unquote(value)

def parse_val(inp:str) -> tuple[str, str]:
    if inp.startswith(BEGIN_MAP):
        print("map -- \nbegin-map")
        return BEGIN_MAP, inp.removeprefix(BEGIN_MAP)
    try:
        value_len = re.search(r'(,|>\))', inp).start()
    except AttributeError:
        error("Expected ',' or '>)' after 'key:value'")

    value = inp[:value_len]
    # Check if num
    if re.fullmatch(r'(0|1)*', value):
        decoded_value = decode_num(value)
        print(f"num -- {decoded_value}")
    # Check if simple string
    elif re.fullmatch(r'([a-zA-Z0-9 \t])*s', value):
        decoded_value = decode_simple(value)
        print(f"string -- {decoded_value}")
    # Check if complex string
    elif re.fullmatch(r'([a-zA-Z]|%[0-9A-F]{2})*%[0-9A-F]{2}([a-zA-Z]|%[0-9A-F]{2})*', value):
        decoded_value = decode_complex(value)
        print(f"string -- {decoded_value}")
    else:
        error("Invalid data type encoding: '{value}'")

    return decoded_value, inp[value_len:]

def main():
    if len(sys.argv) < 2:
        error("No input file provided to command line input")

    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as input_file:
            input_str = input_file.read()
    except FileNotFoundError:
        error(f"FileNotFoundError No such file or directory: '{filepath}'")

    input_str = input_str.strip()
    # Check for root level map
    if input_str.startswith(BEGIN_MAP) and len(input_str) > 2:
        input_str = input_str.removeprefix(BEGIN_MAP)
        print("begin-map")
    else:
        error("No root level map found. Maps must be a pair of '(<' and '>)'")

    current_map = {} # Initialized to root level map
    parent_map_stack = []

    while (len(input_str) > 0):
        if input_str[0] in LOWER_ALPHA:
            # Parse key and value
            next_key, input_str = parse_key(input_str)
            if next_key in current_map:
                error("Duplicate key found in map: " + next_key)

            next_val, input_str = parse_val(input_str)
            current_map[next_key] = next_val
            # If start-map jump to beginning of loop
            if next_val == BEGIN_MAP:
                parent_map_stack.append(current_map)
                current_map = {}
                continue
        # Else if input starts with >)
        elif input_str.startswith(END_MAP):
            print("end-map")
            input_str = input_str.removeprefix(END_MAP)
            if len(parent_map_stack) == 0:
                break
            else:
                current_map = parent_map_stack.pop()
        else:
            error("Expected 'key:value' or '>)' after '(<'")

        # If first char is comma
        if input_str.startswith(','):
            # Parse comma
            input_str = input_str.removeprefix(',')

            # If next char is alpha jump to beginning of loop
            if input_str[0] in LOWER_ALPHA:
                continue
            else:
                error("Expected key name in lowercase alpha after ','")
        # Else if starts with >) jump to beginning of loop
        elif input_str.startswith(END_MAP):
            continue
        # Else ERROR
        else: # FIXME -- This error message may be redundant with parse_val()
            error("Expected ',' or '>)' after 'key:value'")

    if len(input_str) > 0:
        error("Unexpected symbols found after end of root level map.")
    if len(parent_map_stack) > 0:
        error("At least one '>)' missing at end of input")

main()