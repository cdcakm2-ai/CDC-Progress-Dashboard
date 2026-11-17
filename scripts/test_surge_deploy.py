import subprocess
import time
import os

print("Testing surge non-interactive deployment...")
email = "akmeemana.praja.gov@gmail.com"
password = "AkmeemanaPraja2026Secure!"
domain = "akmeemana-praja.surge.sh"

cmd = ["npx", "surge", ".", domain]
p = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    shell=True
)

# Read output and supply input when prompted
output = ""
start = time.time()
while time.time() - start < 30:
    if p.poll() is not None:
        break
    try:
        # Check if process is waiting for input
        line = p.stdout.readline()
        if line:
            print("STDOUT:", line.strip())
            output += line
            if "email:" in line.lower():
                print("Sending email...")
                p.stdin.write(f"{email}\n")
                p.stdin.flush()
            elif "password:" in line.lower():
                print("Sending password...")
                p.stdin.write(f"{password}\n")
                p.stdin.flush()
    except Exception as e:
        print("Err:", e)
        break

stdout, stderr = p.communicate(timeout=10)
print("FINAL STDOUT:", stdout)
print("FINAL STDERR:", stderr)
