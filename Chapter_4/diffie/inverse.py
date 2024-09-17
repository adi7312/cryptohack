def inverse(a,n):
    for x in range(n):
        if (a * x) % n == 1:
            return x


print(inverse(209,991))
