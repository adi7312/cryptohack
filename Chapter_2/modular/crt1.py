from sympy.ntheory.modular import crt

u = [2,3,5]
v = [5,11,17]
res = crt(u,v)[0] % 935

print(res)
