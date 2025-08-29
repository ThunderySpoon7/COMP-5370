import sys

ZERO_BYTE = 48
ONE_BYTE = 49

# Read a two character begin map sequence '(<' from the front of the input string.
def parse_begin(_input_bytes):
    res = _input_bytes
    if (_input_bytes.startswith(b'(<')):
            res = _input_bytes.removeprefix(b'(<')
            print('begin-map')

            # Check after beginning of map
            if (not _input_bytes[:1].isalpha()) or (not _input_bytes.startswith(b'(<')):
                print('ERROR -- Unexpected character found after map start sequence -->\'(<' + _input_bytes[:10], file=sys.stderr)
                exit(66)
    return res

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

# Parses key/value pair from input bytes string
def parse_kv(_input_bytes:bytes):
    res = _input_bytes
    if res[:1].isalpha():
        try:
            colon_idx = res.index(b':')
        except ValueError:
            # FIXME -- Add error message
            exit(66)
            
        key = res[:colon_idx]
        res = res.removeprefix(res[:(colon_idx+1)])

        if not (key.islower() and key.isalpha()):
            print('ERROR -- Keys must only contain lowercase ascii letters a-z', file=sys.stderr)
            exit(66)

        val_end_pos = None
        if (b',' in res) and (b'>)' in res):
            val_end_pos = min(res.index(b','), res.index(b'>)'))
        elif (b',' in res):
            val_end_pos = res.index(b',')
        elif (b'>)' in res):
            val_end_pos = res.index(b'>)')
        else:
            # FIXME -- IDK if this is a good error message
            print('ERROR -- Missing symbol. Expected \'>)\' at end of map.', file=sys.stderr)
            exit(66)

        val = res[:val_end_pos]
        res = res.removeprefix(val)

        val = process_val(val)

# Parses a ',' delimiter separating two key/value pairs
def parse_delim(_input_bytes):
    res = _input_bytes
    if (_input_bytes.startswith(b',')):
            res = _input_bytes.removeprefix(b',')

            if (not _input_bytes[:1].isalpha()) or (not _input_bytes.startswith(b'(<')):
                print('ERROR -- Unexpected character found after comma separator -->\',' + _input_bytes[:10], file=sys.stderr)
                exit(66)
    return res

def parse_key(ib:bytes):
    try:
        colon_idx = ib.index(b':')
    except ValueError:

        # FIXME -- Add error message
        exit(66)

def main():
    # FIXME -- not sure if this is out of scope of the project
    if len(sys.argv) < 2:
        print('ERROR -- Filepath argument not set. Usage: python3 main.py filepath', file=sys.stderr)
        exit(1)
    
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
    # FIXME -- Ask if root level map is strictly required
    if input_bytes.startswith(b'(<'):
        input_bytes = input_bytes.removeprefix(b'(<')
    else:
        print('ERROR -- No root level map found. Input must start with \'(<\')', file=sys.stderr)
        exit(66)

    nesting_depth = 0 # FIXME -- may not need this variable
    current_map = {} # Initialized to root level map
    parent_map_trace = [current_map]

    # Parse loop
    while (len(input_bytes) > 0):
        pass

        # If first char of input is lower alpha
            # Parse key and value
            # If start-map jump to beginning of loop
            # Else continue
        # Else if input starts with >)
            # Parse end-map
        # Else ERROR

        #### Probably need to check if we're done with the input

        # If first char is comma
            # Parse comma
            # If next char is alpha jump to beginning of loop
            # Else ERROR
        # Else if starts with >) jump to beginning of loop
        # Else ERROR

    if (nesting_depth != 0):
        print('ERROR -- Missing symbol. Expected \'>)\' at end of map.', file=sys.stderr)
        exit(66)

main()