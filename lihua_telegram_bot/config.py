import os as _os
import socket as __socket
from configparser import ConfigParser
from platform import system as _system

__v4 = __socket.socket(__socket.AF_INET, __socket.SOCK_DGRAM)
__v6 = __socket.socket(__socket.AF_INET6, __socket.SOCK_DGRAM)
try:
    __v4.connect(("8.8.8.8", 80))
    IPv4 = __v4.getsockname()[0]
except OSError:
    IPv4 = None
try:
    __v6.connect(("2001:4860:4860::8888", 80))
    IPv6 = __v6.getsockname()[0]
except OSError:
    IPv6 = None


class Config:
    WEBHOOK = _os.getenv("lihua_tgbot_ssl", "1")
    TOKEN = _os.getenv("lihua_tgbot_token")
    RHOST = _os.getenv("lihua_tgbot_rhost", IPv4)
    RPOST = _os.getenv("lihua_tgbot_rpost", "8443")
    LHOST = _os.getenv("lihua_tgbot_lhost", "0.0.0.0")
    LPOST = _os.getenv("lihua_tgbot_lpost", RPOST)
    _instance = None

    def __new__(cls, path=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, path=None):
        if not path:
            if _system() != "Linux":
                return
            for path in (
                "config.ini",
                "~/lihua_telegram_bot.ini",
                f'{_os.getenv("XDG_CONFIG_HOME", "~/.config")}/lihua_telegram_bot/config.ini',
                "/etc/lihua_telegram_bot/config.ini",
            ):
                if _os.access(path, _os.R_OK):
                    break
            else:
                return
        config = ConfigParser()
        config.read(path)
        if "DEFAULT" not in config:
            return
        config = config["DEFAULT"]
        self.WEBHOOK = config.getboolean("webhook", self.WEBHOOK)
        self.TOKEN = config.get("token", self.TOKEN)
        self.RHOST = config.get("rhost", self.RHOST)
        self.RPOST = config.get("rpost", self.RPOST)
        self.LHOST = config.get("lhost", self.LHOST)
        self.LPOST = config.get("lpost", self.LPOST)
