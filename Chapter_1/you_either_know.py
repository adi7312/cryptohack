from Crypto.Util.number import long_to_bytes

data = long_to_bytes(0x0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104)


def find_pattern(data):
	possible_key = [0,0,0,0,0,0,0]
	for key in range(0x0, 0xff):
		if (chr(data[0]^key) == 'c'):
			possible_key[0] = chr(key)
		if (chr(data[1]^key) == 'r'):
			possible_key[1] = chr(key)
		if (chr(data[2]^key) == 'y'):
			possible_key[2] = chr(key)
		if (chr(data[3]^key) == 'p'):
			possible_key[3] = chr(key)
		if (chr(data[4]^key) == 't'):
			possible_key[4] = chr(key)
		if (chr(data[5]^key) == 'o'):
			possible_key[5] = chr(key)
		if (chr(data[6]^key) == '{'):
			possible_key[6] = chr(key)
	key = ''.join(possible_key)
	return key

def pad(key):
	return key + 'y'

def decrypt(data, key):
	result = ""
	for i in range(len(data)):
		result += chr(data[i] ^ ord(key[i%len(key)]))
	print(result)

if __name__ == '__main__':
	key = pad(find_pattern(data))
	decrypt(data, key)
