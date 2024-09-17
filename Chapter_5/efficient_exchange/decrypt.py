from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
from ecc import *

def sqrt(x, q):
    for i in range(1, q):
        if pow(i, 2) % q == x:
            return (i, q - i)
    return None

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
        return plaintext.decode("latin-1")

A=497
B=1768
p=9739
curve = ElipticCurve(A,B,p)
G = Point(curve,1804,5368)

def find_y2(x: int):
    return sqrt((x**3 + A*x + B) % p,p)

shared_secret = 0
n_b = 6534
x_Q_A = 4726
y1,y2 = find_y2(x_Q_A)
Q1 = Point(curve,x_Q_A,y1)
Q2 = Point(curve,x_Q_A,y2)
if Q1.y % 4 == 3:
    shared_secret = Q1 * n_b
else:
    shared_secret = Q2 * n_b

print(shared_secret)

iv = 'cd9da9f1c60925922377ea952afc212c'
ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

print(decrypt_flag(shared_secret.x, iv, ciphertext))
