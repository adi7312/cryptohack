import requests
from pwn import xor
def encrypt() -> str:
    return requests.get("https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag").json()["ciphertext"]

def decrypt(ciphertext: str) -> str:
    return requests.get(f"https://aes.cryptohack.org/ecbcbcwtf/decrypt/{ciphertext}/").json()["plaintext"]

FLAG = encrypt()
BLOCKS = [FLAG[i:i+32] for i in [0,32,64]]

def crack():
    iv = BLOCKS[0]
    enc_blocks = BLOCKS[1:]
    decrypted = []
    for block in enc_blocks:
        decrypted.append(decrypt(block))
    plaintext_1 = xor(bytes.fromhex(decrypted[0]), bytes.fromhex(iv))
    plaintext_2 = xor(bytes.fromhex(decrypted[1]), bytes.fromhex(enc_blocks[0]))
    return plaintext_1 + plaintext_2

print(crack())
    




