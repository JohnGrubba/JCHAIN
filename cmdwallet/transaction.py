from ed25519 import SigningKey
from binascii import hexlify, unhexlify
from hashlib import sha256


class Transaction:
    def __init__(self, sender, receiver, amount, private_key, prev_hash="0x") -> None:
        self.private_key = private_key
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.prev_hash = prev_hash
        pass

    def json(self) -> dict:
        block = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
        }
        block_hash = sha256(str(block).encode("utf-8")).hexdigest()
        sk = SigningKey(unhexlify(self.private_key))
        sig = sk.sign(msg=unhexlify(block_hash))
        signature = hexlify(sig).decode()
        return {
            "action": "send",
            "block": block,
            "signature": signature,
            "block_hash": block_hash,
        }
