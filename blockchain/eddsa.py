# twisted edwards curve form: a*x^2 + y^2 = 1 + b*x^2*y^2
import random
from blockchain.keccak import sha3
import hashlib

# EdDSA base functions
def point_mul(P, Q, a, b, m):
    x1, y1 = P
    x2, y2 = Q

    x3 = (((x1 * y2 + x2 * y1) % m) * pow((1 + b * x1 * x2 * y1 * y2), -1, m)) % m
    y3 = (((y1 * y2 - a * x1 * x2) % m) * pow((1 - b * x1 * x2 * y1 * y2), -1, m)) % m

    on_curve((x3, y3), m)

    return x3, y3

def on_curve(P, m):
    x, y = P
    assert (a * x * x + y * y) % m == (1 + b * x * x * y * y) % m

def double_and_add(P, k, a, b, m):
    binary = bin(k)[2:]
    res = P

    for i in range(1, len(binary)): # starts from 1 since stating point is the 1st iteration
        current = binary[i : i+1]
        res = point_mul(res, res, a, b, m) # doubling if bit is 0
        if current == "1": # adding if bit is 1
            res = point_mul(res, P, a, b, m)
    on_curve(res, m)

    return res

# Ed25519 parameters:
# formula params: modulo, a, and b
m = pow(2, 255) - 19
a = -1
b = (-121665 * pow(121666, -1, m)) % m

# genesis point params: point I(x0, y0)
u = 9
y0 = ((u-1) * pow((u+1), -1, m)) % m
x0 = 15112221349535400772501151409588531511454012693041857206046113283949847762202
I = (x0, y0)

# EdDSA processing functions
def hex_to_int(text):
    return int(text, 16)

def str_to_int(text):
    encoded_hex = text.encode("utf-8").hex()
    return hex_to_int(encoded_hex)

def hashing(text_int):
    return int(hashlib.sha256(str(text_int).encode("utf-8")).hexdigest(), 16)

def keypair_gen(bit_size=256):
    pri = random.getrandbits(bit_size)
    pub = double_and_add(I, pri, a, b, m)
    return pub, pri

def sign(msg, pub, pri):
    k1 = hex_to_int(sha3(str(sha3(msg, 256)) + msg, 256)) % m
    # k1 = hashing(hashing(str_to_int(msg)) + str_to_int(msg)) % m
    SignA = double_and_add(I, k1, a, b, m)

    k2 = (SignA[0] + pub[0] + str_to_int(msg)) % m
    SignB = (k1 + k2 * pri)

    signature = (SignA, SignB)

    return signature

def verify(msg, signature, pub):
    SignA, SignB = signature
    k2 = (SignA[0] + pub[0] + str_to_int(msg)) % m
    P1 = double_and_add(I, SignB, a, b, m)
    P2 = point_mul(SignA, double_and_add(pub, k2, a, b, m), a, b, m)
    assert P1[0] == P2[0] and P1[1] == P2[1]
    print("Signature is verified!")

# Test drive
if __name__ == "__main__":
    testpub, testpri = keypair_gen()
    print(testpub)
    print(testpri)
    msg = "aku butuh senapan!"
    s = sign(msg, testpub, testpri)
    print(s)
    verify(msg, s, testpub)
