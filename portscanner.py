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

range_input = input("Please enter the port range (e.g. 1-100 or 100): ").strip()
try:
    if "-" in range_input:
        start_str, end_str = range_input.split("-", 1)
        start = int(start_str)
        end = int(end_str)
    else:
        start = 1
        end = int(range_input)

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

socket.setdefaulttimeout(1)

open_ports = []
total_ports = end - start + 1

try:
    for idx, port in enumerate(range(start, end + 1), start=1):
        # Print progress on a single line (overwrites previous)
        progress_text = f"Checking port {idx}/{total_ports} (port {port})"
        print(progress_text, end="\r", flush=True)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = s.connect_ex((target, port))
            if result == 0:
                # Clear the progress line, then print the open-port message
                clear_line = " " * max(len(progress_text), 60)
                print(clear_line, end="\r", flush=True)
                print(f"Port {port} open")
                open_ports.append(port)
            # if closed: do nothing other than update the progress line
        finally:
            s.close()
    # After loop, ensure cursor moves to next line cleanly
    print()  # newline after the last progress overwrite
except KeyboardInterrupt:
    print("\nExiting Program !!!")
    sys.exit()
except socket.error:
    print("\nServer not responding !!!")
    sys.exit()

# Optional summary
print("-" * 50)
if open_ports:
    print("Open ports found:", ", ".join(str(p) for p in open_ports))
else:
    print("No open ports found in the scanned range.")
print("Scan ended at:", str(datetime.now()))
print("-" * 50)
