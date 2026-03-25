import subprocess
import sys

capture_file = "/tmp/rx_output.dat"
result_file = "/tmp/result.json"

cmd = [
    "python3",
    "analyze.py",
    "--input", capture_file,
    "--output", result_file,
]

completed = subprocess.run(cmd, capture_output=True, text=True)

print("[RX] Analysis stdout:")
print(completed.stdout)

if completed.stderr:
    print("[RX] Analysis stderr:", file=sys.stderr)
    print(completed.stderr, file=sys.stderr)

if completed.returncode != 0:
    raise RuntimeError(f"Analysis failed with return code {completed.returncode}")

print(f"[RX] Analysis complete. JSON result written to {result_file}")