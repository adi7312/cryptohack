import requests
from pwn import log

def get_enc_flag():
    return requests.get("https://aes.cryptohack.org/symmetry/encrypt_flag").json()["ciphertext"]

def encrypt(hex_data: str, iv: str) -> str:
    return requests.get(f"https://aes.cryptohack.org/symmetry/encrypt/{hex_data}/{iv}").json()["ciphertext"]


def crack():
    """
    Encryption process in AES-OFB mode can be determined using following equation:
    C = enc(IV) ^ FLAG
    Decryption:
    FLAG = enc(IV) ^ C
    OFB weakness relies on fact that performing encryption/decryption takes same operations,
    so to decrypt flag, we need to pass ciphertext and iv into encrypt function.
    """
    iv_flag = get_enc_flag()
    IV = iv_flag[:32]
    FLAG = iv_flag[32:]
    return bytes.fromhex(encrypt(FLAG, IV))

print(crack())
