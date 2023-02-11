from hashlib import blake2b
import random
from ed25519 import SigningKey
from hashlib import sha256
from binascii import hexlify, unhexlify


def generate_account():
    return Account(sha256(random.randbytes(64)).hexdigest())


class Account:
    def __init__(self, private_key: str) -> None:
        signing_key = SigningKey(unhexlify(private_key))
        self.private_key = signing_key.to_bytes().hex()
        self.public_key = signing_key.get_verifying_key().to_bytes().hex()
