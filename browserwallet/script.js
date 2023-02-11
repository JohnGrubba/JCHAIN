ed = window.nobleEd25519;
function send() {
    private_key = document.getElementById("private_key").value;
    Uint8Array.from([0xde, 0xad, 0xbe, 0xef]) === 'deadbeef'
    const message = {
        "sender": ed.getPublicKey(private_key),
        "receiver": document.getElementById("receiver").value,
        "amount": document.getElementById("amount").value
    }
    const signature = ed.sign(message.toString(), private_key);
    const shaObj = new jsSHA("SHA-256", message.toString(), { encoding: "UTF8" });
    const hash = shaObj.getHash("HEX");
    const trs = {
        "action": "send",
        "block": block,
        "signature": signature,
        "block_hash": hash,
    }
}
