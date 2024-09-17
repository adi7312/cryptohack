from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import json
from pwn import *
from sympy.ntheory import discrete_log

io = remote("socket.cryptohack.org",13379)

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

io.recvuntil(b"Intercepted from Alice: ")
supported = json.dumps({"supported": ["DH64"]})
io.sendline(bytes(supported.encode("utf-8")))
io.recvuntil(b"Intercepted from Bob: ")
chosen = io.recvline()
io.sendline(chosen)
io.recvuntil(b"Intercepted from Alice: ")
alice = json.loads(io.recvline().decode("utf-8"))
io.recvuntil(b"Intercepted from Bob: ")
B = int(json.loads(io.recvline().decode("utf-8"))['B'],0)
io.recvuntil(b"Intercepted from Alice: ")
flag_alice = json.loads(io.recvline().decode("utf-8"))
p = int(alice['p'],0)
g = 2
A = int(alice['A'],0)
log.info(f"p: {p}")
log.info(f"A: {A}")
log.info(f"B: {B}")
log.info(f"g: 0x2")

a = discrete_log(p,A,g)
log.info(f"a: {a}")
shared_secret = pow(B,a,p)
log.info(f"Shared secret: {shared_secret}")
iv = flag_alice['iv']
ciphertext = flag_alice['encrypted_flag']

log.success(f"Found flag: {decrypt_flag(shared_secret, iv, ciphertext)}")


