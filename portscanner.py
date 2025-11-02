import pyfiglet
import sys
import socket
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("Port Scanner")
print(ascii_banner)

if len(sys.argv) == 2:
  target = socket.gethostbyname(sys.argv[1])
else:
  print("invalid amount of arguments")
  