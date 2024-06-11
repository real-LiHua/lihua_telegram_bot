# pylint: disable=C0411,C0413
from lihua_telegram_bot.config import Config

config = Config()
if not config.WEBHOOK:
    # pylint: disable=E0704
    raise
import datetime
import os.path
from tempfile import mkdtemp

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# pylint: disable=C0412
from lihua_telegram_bot.log import logger

logger.debug("正在创建临时目录")
tmp = mkdtemp()
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

logger.debug("正在生成私钥")
with open(os.path.join(tmp, "private.key"), "wb") as f:
    _key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    print(_key.decode())
    f.write(_key)

name = x509.Name(
    [
        x509.NameAttribute(NameOID.COMMON_NAME, config.RHOST),
    ]
)

cert = (
    x509.CertificateBuilder()
    .subject_name(name)
    .issuer_name(name)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=10))
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False
    )
    .sign(key, hashes.SHA256())
)

logger.debug("正在生成证书")
with open(os.path.join(tmp, "cert.pem"), "wb") as f:
    cert = cert.public_bytes(serialization.Encoding.PEM)
    print(cert.decode())
    f.write(cert)
