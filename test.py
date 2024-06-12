import random
from blockchain.eddsa import keypair_gen, sign, verify
from blockchain.ecies import raise_pub, raise_pri, enc, dec
from blockchain.keccak import sha3
import time

if __name__ == "__main__":
    # stopwatch start:
    start = time.time()

    # EdDSA Testing
    testpub, testpri = keypair_gen()
    print("Public Key: ", testpub)
    print("Private Key: ", testpri)
    msg = "aku butuh senapan!"
    print("Plain Text: ", msg)
    s = sign(msg, testpub, testpri)
    print("Digital Signature: ", s)
    print("Verification Status: ")
    verify(msg, s, testpub)

    # ECIES Testing
    rA = random.getrandbits(256)
    rB = random.getrandbits(256)
    print("A's secret random key: ", rA)
    print("B's secret random key: ", rB)
    pubA = raise_pub(rA)
    pubB = raise_pub(rB)
    print("A's public key: ", pubA)
    print("B's public key: ", pubB)
    prvB = raise_pri(pubA, rB)
    print("B's private key (needed for encryption): ", prvB)
    msg = "tolong aku!"
    print("Plain Text: ", msg)
    ct = enc(msg, "sekarang", prvB)
    print("Cipher Text: ", ct)
    res = dec(ct, "sekarang", pubB, rA)
    print("Decrypted Text: ", res)

    # Keccak Testing
    print(sha3("kerja bagus!", 256))

    # stopwatch end:
    end = time.time()

    # time elapsed:
    print("Time elasped to execute the test is : ", (end-start) , "s")