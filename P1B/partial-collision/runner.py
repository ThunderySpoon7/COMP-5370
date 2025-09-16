import subprocess
import time
import sys

TIMEOUT = 12 * 60 * 60

print("Starting Program...\n")

start_time = time.perf_counter_ns()

try:
    res = subprocess.run(
            ["make", "run"],
            capture_output=True,
            timeout=TIMEOUT
            )
except (TimeoutError):
    print("ERROR -- TIMEOUT program took longer than 12 hours", file=sys.sterr)
    exit(1)

elapsed_time = (time.perf_counter_ns() - start_time) / 1_000_000
s, ms = divmod(elapsed_time, 1000)
m, s = divmod(s, 60)
h, m = divmod(m, 60)

print(res.stdout.decode())
print(f"Done. Elapsed Time: {int(h):d}:{int(m):02d}:{int(s):02d}.{int(ms):03d}")