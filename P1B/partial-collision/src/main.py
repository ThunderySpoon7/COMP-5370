from hashlib import sha256
import random
import base64
import sys # FIXME -- Remove

PREFIX = b"nab0063@auburn.edu"
SUFFIX_LENGTH = 32 - len(PREFIX)
TRAIL_THRESH = 2

def get_random_suffix() -> bytes:
    return random.randbytes(SUFFIX_LENGTH)

def get_random_input() -> bytes:
    return PREFIX + get_random_suffix()

def validate_partial_collision(d1: str, d2: str) -> bool:
    return d1[-2*TRAIL_THRESH:] == d2[-2*TRAIL_THRESH:] # Checks if trails match

def validate_trail_pattern(digest: str) -> bool:
    trail = digest[-2*TRAIL_THRESH:]
    return len(set([trail[i:i+2] for i in range(0, len(trail), 2)])) == 1 # Checks if all bytes in trail are the same

def bytes_to_b64(inp: bytes) -> str:
    return base64.b64encode(inp).decode()

def write_to_file(dest: str, output: str) -> None:
    with open(dest, "w") as outfile:
        outfile.write(output)

def main():
    match sys.argv[1]:
        case 1:
            while True:
                inp1, inp2 = get_random_input(), get_random_input()
                dig1, dig2 = sha256(inp1).hexdigest(), sha256(inp2).hexdigest()

                if validate_partial_collision(dig1, dig2) and validate_trail_pattern(dig1):
                    break
        case 2:
            while True:
                inp1 = get_random_input()
                dig1 = sha256(inp1).hexdigest()

                if validate_trail_pattern(dig1):
                    inp2 = get_random_input()
                    dig2 = sha256(inp2).hexdigest()

                    if validate_partial_collision(dig1, dig2):
                        break
        
    print(f"INPUT 1 -- {bytes_to_b64(inp1)}")
    print(f"INPUT 2 -- {bytes_to_b64(inp2)}")
    
    write_to_file("1-input.txt", bytes_to_b64(inp1))
    write_to_file("2-input.txt", bytes_to_b64(inp2))
    write_to_file("1-sha256-digest.txt", dig1)
    write_to_file("2-sha256-digest.txt", dig2)

if __name__ == "__main__":
    main()