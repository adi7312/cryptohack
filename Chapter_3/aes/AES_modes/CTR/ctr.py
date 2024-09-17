import requests

def encrypt():
    return requests.get("https://aes.cryptohack.org/bean_counter/encrypt/").json()["encrypted"]


def determine_nonce(hex_data: str) -> list:
    PNG_HEADER = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00 ,0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52]
    first_block = list(bytes.fromhex(hex_data))[:16]
    nonce = list()
    for i in range(len(PNG_HEADER)):
        nonce.append(PNG_HEADER[i] ^ first_block[i])
    return nonce

def crack():
    FLAG = encrypt()
    NONCE = determine_nonce(FLAG)
    bytes_flag = bytes.fromhex(FLAG)
    result = [0]*len(bytes_flag)
    for i in range(len(bytes_flag)):
        result[i] = bytes_flag[i] ^ NONCE[i%16]
    with open("bean_counter.png","wb") as f:
        f.write(bytes(result))

crack()

