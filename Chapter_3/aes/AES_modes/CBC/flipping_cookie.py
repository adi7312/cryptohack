import requests
from datetime import datetime, timedelta

def get_cookie() -> str:
    return requests.get("https://aes.cryptohack.org/flipping_cookie/get_cookie/").json()["cookie"]

def check_admin(cookie: str, iv: str) -> str:
    resp = requests.get(f"https://aes.cryptohack.org/flipping_cookie/check_admin/{cookie}/{iv}/").json()
    return resp

def crack():
    expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    cookie = bytes.fromhex(get_cookie())
    original = f'admin=False;expiry={expires_at}'.encode("latin-1")
    tampered = b';admin=True;'
    tampered_enc_data = list(cookie)
    tampered_iv = [0xff]*16
    for i in range(len(tampered)):
        tampered_enc_data[16+i] = tampered[i] ^ original[16+i] ^ tampered_enc_data[16+i]
        tampered_iv[i] = tampered[i] ^ tampered_enc_data[i] ^ original[i]
    
    return bytes(tampered_enc_data).hex(), bytes(tampered_iv).hex()

c, iv = crack()
print(c)
print(iv)
res = check_admin(c,iv)
print(res)




    



