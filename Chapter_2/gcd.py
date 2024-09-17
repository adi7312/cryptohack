def gcd(x:int,y:int) -> int:
    return gcd(y%x,x) if x else y

print(gcd(66528,52920))
