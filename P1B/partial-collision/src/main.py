from hashlib import sha256
from multiprocessing import Process, Manager, managers as _man_
import time, random, base64, os

PREFIX = b"nab0063@auburn.edu"
SUFFIX_LENGTH = 32 - len(PREFIX)
TRAIL_THRESH = 3
MAX_PROCESSES = 8

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

def task(input_digest_list: _man_.ListProxy, lock):
    while True:
        inp1 = get_random_input()
        dig1 = sha256(inp1).hexdigest()
        if validate_trail_pattern(dig1): break
    while True:
        inp2 = get_random_input()
        dig2 = sha256(inp2).hexdigest()
        if validate_partial_collision(dig1, dig2): break
    with lock:
        if len(input_digest_list) == 0:
            input_digest_list.append(inp1)
            input_digest_list.append(inp2)
            input_digest_list.append(dig1)
            input_digest_list.append(dig2)

    

    

def main():
    with Manager() as manager:
        input_digest_list = manager.list()
        lock = manager.Lock()

        procs = [Process(target=task, args=(input_digest_list, lock)) for _ in range(MAX_PROCESSES)]

        for p in procs: p.start()
        while True:
            with lock:
                if len(input_digest_list) != 0:
                    break
            time.sleep(0.1)

        for p in procs:
            if p.is_alive():
                p.terminate()

        for p in procs:
            p.join()

        print(f"INPUT 1 -- {bytes_to_b64(input_digest_list[0])}")
        print(f"INPUT 2 -- {bytes_to_b64(input_digest_list[1])}")
        
        write_to_file("1-input-1.txt", bytes_to_b64(input_digest_list[0]))
        write_to_file("2-input-1.txt", bytes_to_b64(input_digest_list[1]))
        write_to_file("1-sha256-digest-1.txt", input_digest_list[2])
        write_to_file("2-sha256-digest-1.txt", input_digest_list[3])

if __name__ == "__main__":
    main()