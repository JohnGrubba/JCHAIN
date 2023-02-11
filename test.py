from ed25519 import SigningKey, VerifyingKey, BadSignatureError
from binascii import hexlify, unhexlify
from hashlib import sha256

from cmdwallet.account import Account, generate_account

# Initialize Account
acc = Account("5d89eb2db11512b378f9e9017f317a32882f5520c2abf736a6d50836c2183d90")
print(acc.public_key)
print(acc.private_key)

# Transaction
data = {"test": "test"}
block_hash = sha256(str(data).encode("utf-8")).hexdigest()

# Create Signature of data
sk = SigningKey(unhexlify(acc.private_key))
sig = sk.sign(msg=unhexlify(block_hash))
signature = hexlify(sig).decode()

# Verify Transaction (Server)
vk = VerifyingKey(unhexlify(acc.public_key))
vk.verify(sig=unhexlify(signature), msg=unhexlify(block_hash))
