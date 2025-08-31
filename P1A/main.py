import sys

ZERO_BYTE = 48
ONE_BYTE = 49
BIN_BYTES = [48, 49]
LOWER_ALPHA = [i for i in range(0x61, 0x7b)]
BEGIN_MAP = b'(<'
END_MAP = b'>)'
COMMA_BYTE = 44

# Parse and convert base-10 value from two's compliment binary string
def parse_num(v:bytes):
    res = 0
    try:
        return str(int(v.decode(), 2) - (1 << len(v) if v[0] == ONE_BYTE else 0)).encode()
    except ValueError:
        print('ERROR -- Type num value must be represented in twos compliment binary', file=sys.stderr)
        exit(66)

# Process value v as a num, simple string, or complex string. 
# Throws error if incorrectly formatted.
def process_val(v:bytes):
    if (v.startswith(b' ') or v.endswith(b' ')):
        # FIXME -- Print error message
        exit(66)

    res = None
    # Parse num
    if (v.isdigit()):
        return parse_num(v)

    # Parse simple string

    # Parse complex string

def parse_key(inp:bytes) -> tuple[bytes, bytes]:
    # FIXME -- Implement
    try:
        colon_idx = inp.index(b':')
    except ValueError:

        # FIXME -- Add error message
        exit(66)

def parse_val(inp:bytes) -> tuple[bytes, bytes]:
    pass
    # FIXME -- Implement

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
        else:
            print("ERROR -- Expected ',' or '>)' after 'key:value'", file=sys.stderr)
            exit(66)

    if (nesting_depth != 0):
        print('ERROR -- Missing symbol. Expected \'>)\' at end of map.', file=sys.stderr)
        exit(66)

main()