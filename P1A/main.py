import sys, re
from urllib.parse import unquote

ZERO_BYTE = 48
ONE_BYTE = 49
BIN_BYTES = [48, 49]
LOWER_ALPHA = [i for i in range(0x61, 0x7b)]
BEGIN_MAP = b'(<'
END_MAP = b'>)'
COMMA_BYTE = 44

def validate_key(key:bytes):
    if not (key.islower() and key.isalpha()):
        print(f"ERROR -- Keys must be lowercase alpha strings. Found key: '{key.decode()}'", file=sys.stderr)
        exit(66)

# Parses and removes key and ':' from inp
# returns key, modified inp
def parse_key(inp:bytes) -> tuple[bytes, bytes]:
    try:
        key_len = inp.index(b':')
    except ValueError:
        print("ERROR -- Expected ':' separating key and value", file=sys.stderr)
        exit(66)
    
    key = inp[:key_len]
    validate_key(key)

    return key, inp[key_len+1:]

def decode_num(value:bytes) -> bytes:
    try:
        return str(int(value.decode(), 2) - (1 << len(value) if value[0] == ONE_BYTE else 0)).encode()
    except ValueError:
        print('ERROR -- Type num value must be represented in twos compliment binary', file=sys.stderr)
        exit(66)

def decode_simple(value:bytes) -> bytes:
    return value[:-1]

def decode_complex(value:bytes) -> bytes:
    return unquote(value).encode()

def parse_val(inp:bytes) -> tuple[bytes, bytes]:
    if inp.startswith(BEGIN_MAP):
        return BEGIN_MAP, inp.removeprefix(BEGIN_MAP)
    try:
        value_len = re.search(rb'(,|>\))', inp).start()
    except AttributeError:
        print("ERROR -- Expected ',' or '>)' after 'key:value'", file=sys.stderr)
        exit(66)

    value = inp[:value_len]
    if re.fullmatch(rb'(0|1)*', value):
        value = decode_num(value)
        print(f"num -- {value}")
    elif re.fullmatch(rb'([a-zA-Z0-9 \t])*s', value):
        value = decode_simple(value)
        print(f"string -- {value}")
    elif re.fullmatch(rb'([a-zA-Z]|%[0-9A-F]{2})*%[0-9A-F]{2}([a-zA-Z]|%[0-9A-F]{2})*', value):
        value = decode_complex(value)
        print(f"string -- {value}")
    else:
        print(f"ERROR -- Invalid data type encoding: '{value}'", file=sys.stderr)
        exit(66)

    return value, inp[value_len:]

def main():
    filepath = sys.argv[1]

    try:
        with open(filepath, 'rb') as input_file:
            input_bytes = input_file.read()
    except FileNotFoundError:
        # FIXME -- Apparently not supposed to do this. Ask how/if we should handle FileNotFound
        print('ERROR -- File not found. Check FILE argument.', file=sys.stderr)
        exit(1)

    # Strip leading and trailing whitespace
    input_bytes = input_bytes.strip()

    # Check for root map
    if input_bytes.startswith(BEGIN_MAP):
        input_bytes = input_bytes.removeprefix(BEGIN_MAP)
    else:
        print('ERROR -- No root level map found. Input must start with \'(<\')', file=sys.stderr)
        exit(66)

    nesting_depth = 0 # FIXME -- may not need this variable
    current_map = {} # Initialized to root level map
    parent_map_stack = []

    # Parse loop
    while (len(input_bytes) > 0):
        # If first char of input is lower alpha
        if input_bytes[0] in LOWER_ALPHA:
            # Parse key and value
            next_key, input_bytes = parse_key(input_bytes)
            if next_key in current_map:
                print("ERROR -- Duplicate key found in map: " + next_key.decode())
                exit(66)

            next_val, input_bytes = parse_val(input_bytes)
            current_map[next_key] = next_val
            # If start-map jump to beginning of loop
            if next_val == BEGIN_MAP:
                parent_map_stack.append(current_map)
                current_map = {}
                continue
            # Else next_val is num or string. Proceed
            else:
                # parse_val() should catch any other invalidly formatted values so we should be good here
                # FIXME -- I don't think anything needs to be done here, but I might be wrong
                pass
        # Else if input starts with >)
        elif input_bytes.startswith(END_MAP):
            input_bytes = input_bytes.removeprefix(END_MAP)
            current_map = parent_map_stack.pop()
        # Else ERROR
        else:
            print("ERROR -- Expected 'key:value' or '>)' after '(<'", file=sys.stderr)
            exit(66)

        #### Probably need to check if we're done with the input

        # If first char is comma
        if input_bytes[0] == COMMA_BYTE:
            # Parse comma
            input_bytes = input_bytes.removeprefix(b',')

            # If next char is alpha jump to beginning of loop
            if input_bytes[0] in LOWER_ALPHA:
                continue
            # Else ERROR
            else:
                print("ERROR -- Expected key name in lowercase alpha after ','", file=sys.stderr)
                exit(66)
        # Else if starts with >) jump to beginning of loop
        elif input_bytes.startswith(END_MAP):
            continue
        # Else ERROR
        else: # FIXME -- This error message may be redundant with parse_val()
            print("ERROR -- Expected ',' or '>)' after 'key:value'", file=sys.stderr)
            exit(66)

    if (nesting_depth != 0):
        print('ERROR -- Missing symbol. Expected \'>)\' at end of map.', file=sys.stderr)
        exit(66)

main()