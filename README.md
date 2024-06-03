[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

还没想到要干啥


```bash
openssl req -newkey rsa:2048 -sha256 -noenc -x509 -days 3650 \
            -keyout lihua_telegram_bot/private.key \
            -out lihua_telegram_bot/cert.pem \
            -subj "/CN=$(python -c 'import lihua_telegram_bot.config;print(lihua_telegram_bot.config.IP)')"
python -m lihua_telegram_bot
```
