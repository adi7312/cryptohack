from pwn import log
import requests

PADDED_BLOCK = "9863b1089f6206d6e75e071a1d6574e4"
offset = "DEADBEEFDEADBE"

def generate_bytearray() -> list:
    b = []
    for i in range(1, 256):
        byte = hex(i)[2:] 
        if len(byte)==1: 
            byte = '0' + byte
        b.append(byte)
    return b

bytesarr = generate_bytearray()


def encrypt(plaintext):
    request = requests.get(f"https://aes.cryptohack.org/ecb_oracle/encrypt/{plaintext}")
    return request.json()['ciphertext']


def crack():
    padding_counter = 15
    solution = ""
    payload = offset
    printable_ascii = bytesarr[0x20:0x7E]
    x,y=64,96 # initial boundaries - the last block
    while True:
        payload += "EF"
        encrypted_payload = encrypt(payload)
        last_block = encrypted_payload[x:y]
        if padding_counter == 0:
            x = -64
            y = -32 # boundaries of second-to-last block
            last_block = encrypted_payload[x:y]
            padding_counter = 16
        for b in printable_ascii:
            tmp = b + solution + bytesarr[padding_counter-1]*padding_counter
            encrypted_tmp = encrypt(tmp)
            if (encrypted_tmp[:32] == last_block):
                log.success(f"Found char: {b}")
                solution = b + solution
                break
            else:
                log.info(f"Testing {tmp}")
        if (len(solution) >= 50):
            log.success(f'Flag: {bytes.fromhex(solution).decode("latin-1")}')
        padding_counter -= 1

crack()



