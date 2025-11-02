import pyfiglet
import sys
import socket
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("Port Scanner")
print(ascii_banner)

# Prompt for target instead of requiring a command-line argument
target_input = input("Please enter the target IP or hostname: ").strip()
try:
    target = socket.gethostbyname(target_input)
except socket.gaierror:
    print("Hostname could not be resolved !!!")
    sys.exit()

print("-" * 50)
print("Scanning:", target)
print("Scan started at:", str(datetime.now()))
print("-" * 50)

# Accept either "1-100" or a single number like "100"
range_input = input("Please enter the port range (e.g. 1-100 or 100): ").strip()
try:
    if "-" in range_input:
        start_str, end_str = range_input.split("-", 1)
        start = int(start_str)
        end = int(end_str)
    else:
        # single value -> scan from 1 to this value
        start = 1
        end = int(range_input)

    # Basic validation and clamping to allowed port range
    if start < 1:
        start = 1
    if end > 65535:
        end = 65535
    if end < start:
        print("Invalid range: end < start")
        sys.exit()
except ValueError:
    print("Invalid port range format. Use e.g. 1-100 or 100")
    sys.exit()

# set a global connect timeout (once)
socket.setdefaulttimeout(1)

try:
    for port in range(start, end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} checked: open")
            else:
                print(f"Port {port} checked: closed")
        finally:
            s.close()
except KeyboardInterrupt:
    print("\nExiting Program !!!")
    sys.exit()
except socket.error:
    print("Server not responding !!!")
    sys.exit()
