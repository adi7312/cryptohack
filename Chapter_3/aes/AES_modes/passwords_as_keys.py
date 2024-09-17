from Cryptodome.Cipher import AES
import hashlib
import random

with open("./words") as f:
    words = [w.strip() for w in f.readlines()]

FLAG = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"
def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = password_hash

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return decrypted

for word in words:
    KEY = hashlib.md5(word.encode()).digest()
    decrypted = decrypt(FLAG,KEY)
    if b'crypto' in decrypted:
        print(decrypted)
