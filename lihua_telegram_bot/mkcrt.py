import datetime
from tempfile import mkdtemp

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from lihua_telegram_bot import config

tmp = mkdtemp()
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

with open(f"{tmp}/private.key", "wb") as f:
    f.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

name = x509.Name(
    [
        x509.NameAttribute(NameOID.COMMON_NAME, config.IP),
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
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    .sign(key, hashes.SHA256())
)
with open(f"{tmp}/cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
