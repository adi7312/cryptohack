from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import json
from pwn import *

io = remote("socket.cryptohack.org",13371)

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

alice_init_data = "{" + io.recvuntil(b"}").decode("utf-8").split("{")[1]
alice_dict = json.loads(alice_init_data)
bob_dict = alice_dict
bob_dict['p'] = '0x1'
io.sendline(bytes(json.dumps(bob_dict).encode("utf-8")))

io.recvuntil(b"Intercepted from Bob: ")
line = io.recvline()
print(line)
io.sendline(line)

io.recvuntil(b"Intercepted from Alice: ")
alice_final = json.loads(io.recvline())

print(decrypt_flag(0, alice_final['iv'], alice_final['encrypted_flag']))
