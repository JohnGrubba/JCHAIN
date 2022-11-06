from account import Account, generate_account
from transaction import Transaction
import asyncio, json
import websockets


async def start():
    async with websockets.connect("wss://crypto.jjhost.tk") as websocket:
        acc = Account(
            "5d89eb2db11512b378f9e9017f317a32882f5520c2abf736a6d50836c2183d90"
        )
        acc1 = generate_account()
        print(acc.public_key)
        print(acc.private_key)

        trs = Transaction(acc.public_key, acc1.public_key, 10, acc.private_key)
        print(trs.json())
        await websocket.send(json.dumps(trs.json()))
        print(await websocket.recv())


asyncio.run(start())
