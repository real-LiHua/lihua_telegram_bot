import os as __os
import socket as __socket

__sock = __socket.socket(__socket.AF_INET, __socket.SOCK_DGRAM)
__sock.connect(("8.8.8.8", 80))
IP = __sock.getsockname()[0]
TOKEN = __os.getenv("lihua_telegram_bot")
