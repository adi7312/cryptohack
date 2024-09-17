def find_square_root(p: int, x: int):
    for i in range(1,p-1):
        if (i**2 % p == x):
            return i


print(find_square_root(29, 6))
