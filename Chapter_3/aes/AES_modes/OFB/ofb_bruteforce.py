import requests
from pwn import log

def generate_bytearray() -> list:
    b = []
    for i in range(1, 256):
        byte = hex(i)[2:]
        if len(byte)==1:
            byte = '0' + byte
        b.append(byte)
    return b

bytesarr = generate_bytearray()[0x20:0x7E] # printable ascii

def get_enc_flag():
    return requests.get("https://aes.cryptohack.org/symmetry/encrypt_flag").json()["ciphertext"]

def encrypt(hex_data: str, iv: str) -> str:
    return requests.get(f"https://aes.cryptohack.org/symmetry/encrypt/{hex_data}/{iv}").json()["ciphertext"]

def str_to_hexlist(hex_data: str):
    data_bytes = list(bytes.fromhex(hex_data))
    hexlist = list()
    for i in range(len(data_bytes)):
        literal = hex(data_bytes[i])[2:]
        if (len(literal) == 1):
            literal = '0' + literal
        hexlist.append(literal)
    return hexlist

def crack():
    FLAG = get_enc_flag()
    hex_flag_list = str_to_hexlist(FLAG[32:])
    IV = FLAG[:32]
    solution = ""
    for i in range(len(hex_flag_list)):
        for sb in bytesarr:
            log.info(f"Testing: {solution + sb}")
            enc_sb = encrypt(solution + sb, IV)
            if (enc_sb == ''.join(hex_flag_list[:i+1])):
                log.success(f"Found valid char!: {sb}")
                solution += sb
                log.success(f"Current solution state: {bytes.fromhex(solution)}")
                break

crack()

    
    
