from hashlib import sha256
import random
import base64

PREFIX = b"nab0063@auburn.edu"
SUFFIX_LENGTH = 32 - len(PREFIX)
TRAIL_THRESH = 4

def get_random_suffixes():
    return random.randbytes(SUFFIX_LENGTH), random.randbytes(SUFFIX_LENGTH)

def get_random_inputs_b64():
    suff_1, suff_2 = get_random_suffixes()
    return base64.b64encode(PREFIX + suff_1), base64.b64encode(PREFIX + suff_2)

def check_partial_collision(d1: str, d2: str):
    return d1[-2*TRAIL_THRESH:] == d2[-2*TRAIL_THRESH:]

def write_to_file(dest: str, output: str):
    with open(dest, "w") as outfile:
        outfile.write(output)

def main():
    while True:
        inp_1, inp_2 = get_random_inputs_b64()
        dig_1, dig_2 = [sha256(x).hexdigest() for x in (inp_1, inp_2)]

        if (check_partial_collision(dig_1, dig_2)):
            break
        
    print(f"INPUT 1 -- {inp_1.decode()}")
    print(f"INPUT 2 -- {inp_2.decode()}")
        
    write_to_file("1-input.txt", inp_1.decode())
    write_to_file("2-input.txt", inp_2.decode())
    write_to_file("1-sha256-digest.txt", dig_1)
    write_to_file("2-sha256-digest.txt", dig_2)

if __name__ == "__main__":
    main()