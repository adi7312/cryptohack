init = bytearray("label","latin-1")
key = 13
final = ""

for i in range(len(init)):
	final += chr(init[i] ^ key)

print(final)
