import hashlib
import time
import asyncio
import websockets, json

max_nonce = 2**32


def proof_of_work(header, difficulty_bits):
    target = 2 ** (256 - difficulty_bits)
    for nonce in range(max_nonce):
        hash_result = hashlib.sha256(
            (str(header) + str(nonce)).encode("ascii")
        ).hexdigest()
        if int(hash_result, 16) < target:
            print("Success with nonce %d" % nonce)
            print("Hash is %s" % hash_result)
            return (hash_result, nonce)
    print("Failed after %d (max_nonce) tries" % nonce)
    return nonce


async def start():
    async with websockets.connect("wss://crypto.jjhost.tk") as websocket:
        await websocket.send("Hello world!")
        new_block = json.loads(await websocket.recv())

        nonce = 0
        hash_result = ""
        difficulty_bits = 5
        difficulty = 2**difficulty_bits
        print("Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits))

        print("Starting search...")

        # checkpoint the current time
        start_time = time.time()
        (hash_result, nonce) = proof_of_work(new_block, difficulty_bits)
        end_time = time.time()

        elapsed_time = end_time - start_time
        print("Elapsed Time: %.4f seconds" % elapsed_time)

        if elapsed_time > 0:
            # estimate the hashes per second
            hash_power = float(int(nonce) / elapsed_time)
            print("Hashing Power: %ld hashes per second" % hash_power)
        await websocket.send(hash_result)


asyncio.run(start())
