from Cryptodome.Hash import SHA1


class ElipticCurve:
    def __init__(self, a: int, b: int, p: int):
        self.a = a
        self.b = b
        self.p = p

    def get_point_at_infinity(self):
        return Point(curve=self, x=None, y=None)
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.p == other.p


class Point:
    def __init__(self, curve, x, y):
        if not isinstance(curve, ElipticCurve):
            raise TypError("Invalid type of curve")
        self.curve = curve
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def copy(self):
        return Point(self.curve, self.x, self.y)

    def is_infinity_point(self):
        return self == self.curve.get_point_at_infinity()
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Invalid type of provided point!")
        return self.x == other.x and self.y == other.y and self.curve == other.curve
    
    def __mul__(self, n):
        bits = [n & (1<<i) for i in range(n.bit_length()-1,-1,-1)]
        res = self.curve.get_point_at_infinity()
        for bit in bits:
            res += res
            if bit:
                res = res + self
        return res

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypError("Invalid type of provided point!")
        if self.is_infinity_point():
            return other.copy()
        if other.is_infinity_point():
            return self.copy()

        x1,y1 = self.x, self.y
        x2,y2 = other.x, other.y
        p = self.curve.p
        if x1 %p == x2 %p and y1 % p == (-y2)%p:
            return self.curve.get_point_at_infinity()
        if self != other:
            s = (y2-y1) * pow(x2-x1,-1,p) % p
        else:
            s = (3* pow(x1,2) + self.curve.a) * pow(2*y1,-1,p) % p

        x3 = (pow(s,2) - x1 - x2) % p
        y3 = (s * (x1-x3) - y1) % p
        return Point(self.curve, x3, y3)



