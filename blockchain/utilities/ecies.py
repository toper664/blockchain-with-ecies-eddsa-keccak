# elliptic curve form: y^2 = x^3 + a*x + b
import random
import hashlib
from Crypto.Cipher import AES

# ECIES base functions
def point_mul(P, Q, m):
    x1, y1 = P
    x2, y2 = Q

    # if P == Q then it's point doubling, not point addition
    if x1 == x2 and y1 == y2:
        f = (3 * x1 * x1 + a) * pow((2 * y1), -1, m)
    else: # point addition
        f = (y2 - y1) * pow((x2 - x1), -1, m)
    
    x3 = (f * f - x1 - x2) % m
    y3 = (f * (x1 - x3) - y1) % m

    on_curve((x3, y3), m)

    return x3, y3

def on_curve(P, m):
    x, y = P
    assert (y * y) % m == (pow(x, 3, m) + a * x + b) % m

def double_and_add(P, k, m):
    binary = bin(k)[2:]
    res = P

    for i in range(1, len(binary)): # starts from 1 since stating point is the 1st iteration
        current = binary[i : i+1]
        res = point_mul(res, res, m) # doubling if bit is 0
        if current == "1": # adding if bit is 1
            res = point_mul(res, P, m)
    on_curve(res, m)

    return res

# secp256k1 parameters:
# formula params: a, b, and modulo
a = 0; b = 7
m = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)

# genesis point params: point I(x0, y0)
x0 = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y0 = 32670510020758816978083085130507043184471273380659243275938904335757337482424
I = (x0, y0)

# proof that genesis point is on the curve:
# print(on_curve(I, m)) --> true (no error raised)
# print(point_mul(I, I, m)) --> point 2I is on curve, hence every point will be on curve

# raising key pairs using double and add method is faster than for loops
# ECDLP states that for an instance of Q = k * P
# - knowing k and P will get you Q easily
# - knowing P and Q will NOT get you k easily --> virtually impossible

# ECIES processing functions
def derive_keys(P):
    x0, y0 = P

    xbin = bin(x0)[2:]
    xbin = xbin[:192]

    x1 = int(xbin, 2)

    hexdigest = hashlib.sha256(str.encode(str(x1))).hexdigest()
    bindigest = bin(int(hexdigest, 16))[2:]

    k1 = int(bindigest[:128], 2).to_bytes(16, byteorder="big")
    k2 = int(bindigest[128:], 2).to_bytes(16, byteorder="big")

    return k1, k2

def raise_pub(rand):
    pub = double_and_add(I, rand, m)
    return pub

def raise_pri(pub, rand):
    pri = double_and_add(pub, rand, m)
    return pri

def enc(plain, nonce, pri):
    k1, k2 = derive_keys(pri)
    m = plain.encode("utf-8")
    n = nonce.encode("utf-8")
    c = AES.new(k1, AES.MODE_EAX, n)
    cipher = c.encrypt(m)
    return cipher

def dec(cipher, nonce, sent_pub, pri):
    pri_accent = double_and_add(sent_pub, pri, m)
    n = nonce.encode("utf-8")
    k1_accent, k2_accent = derive_keys(pri_accent)
    d = AES.new(k1_accent, AES.MODE_EAX, n)
    result = d.decrypt(cipher).decode("utf-8")
    return result

# test
# rA = random.getrandbits(256)
# rB = random.getrandbits(256)
# pubA = raise_pub(rA)
# pubB = raise_pub(rB)

# prvB = raise_pri(pubA, rB)

# ct = enc("tolong aku!", "sekarang", prvB)
# res = dec(ct, "sekarang", pubB, rA)
# print(res)