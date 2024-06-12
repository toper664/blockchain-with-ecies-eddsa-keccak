# 18221102 | Salman Ma'arif Achsien
# 18221115 | Christopher Febrian Nugraha

import numpy as np
import random
import math
from sys import exit

# Mengubah array 1D menjadi array 3D
def oneToThree(arr1D):
    arr3D = np.zeros((5, 5, 64), dtype = int) # inisialisasi array 3D dengan ukuran 5x5x64
    for i in range(5):
        for j in range(5):
            for k in range(64):
                arr3D[i][j][k] = arr1D[64*(5*j + i) + k] # input setiap elemen array 1D ke array 3D
    return arr3D

# Mengubah array 3D menjadi 1D
def threeToOne(arr3D):
    arr1D = np.zeros(1600, dtype = int) # inisialisasi array 1D dengan ukuran 1600
    for i in range(5):
        for j in range(5):
            for k in range(64):
                arr1D[64*(5*j+i)+k] = arr3D[i][j][k] # input setiap elemen array 3D ke array 1D
    return arr1D

# Komputasi paritas setiap kolom ukuran 5-bit menjadi dua kolom (disebut juga langkah "Theta" dari fungsi f)
def theta(input):
    output = np.zeros((5, 5, 64), dtype = int) # inisialisasi array output dengan ukuran yang sama dengan input
    for i in range(5):
        for j in range(5):
            for k in range(64):
                # Operasi XOR dengan hasil dari sub-rutin
                a = np.bitwise_xor(input[(i-1)%5][0][k], input[(i-1)%5][1][k])
                b = np.bitwise_xor(input[(i-1)%5][2][k], input[(i-1)%5][3][k])
                c = np.bitwise_xor(a, b)
                part1 = np.bitwise_xor(c, input[(i-1)%5][4][k])
                d = np.bitwise_xor(input[(i+1)%5][0][(k-1)%64], input[(i+1)%5][1][(k-1)%64])
                e = np.bitwise_xor(input[(i+1)%5][2][(k-1)%64], input[(i+1)%5][3][(k-1)%64])
                f = np.bitwise_xor(d, e)
                part2 = np.bitwise_xor(f, input[(i+1)%5][4][(k-1)%64])

                output[i][j][k] = np.bitwise_xor(input[i][j][k], np.bitwise_xor(part1, part2))
    return output

# Rotasi state S menggunakan angka trianguler yang berbeda (disebut juga langkah "Rho" dari fungsi f)
def rho(input):
    triangles = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
    trimat = np.array(triangles, dtype=int) # angka trianguler diatas diubah menjadi np.array
    output = np.zeros((5,5,64), dtype = int) # inisialisasi array output dengan ukuran yang sama dengan input

    for i in range(5):
        for j in range(5):
            for k in range(64):
                curr = trimat[i][j] # mencari angka trianguler untuk kalkulasi
                output[i][j][k] = input[i][j][k - curr]
    return output

# Permutasi state S dalam sebuah pola teratur (disebut juga langkah "Pi" dari fungsi f)
def pi(input):
    output = np.zeros((5,5,64), dtype = int) # inisialisasi array output dengan ukuran yang sama dengan input

    for i in range(5):
        for j in range(5):
            for k in range(64):
                output[j][(2*i+3*j)%5][k] = input[i][j][k]
    return output

# Kombinasi bitwise sepanjang row yang ada menggunakan logika x ← x ⊕ (¬y & z) (disebut juga langkah "Chi" dari fungsi f)
def chi(input):
    output = np.zeros((5,5,64), dtype = int) # inisialisasi array output dengan ukuran yang sama dengan input

    for i in range(5):
        for j in range(5):
            for k in range(64):
                negy = np.bitwise_xor(input[(i+1)%5][j][k], 1)
                withz = negy * (input[(i+2)%5][j][k])
                output[i][j][k] = np.bitwise_xor(input[i][j][k], withz)
    return output

# Operasi XOR bagian dari S dengan bagian dari konstanta ronde LFSR (diesbut juga langkah "Iota" dari fungsi f).
def iota(input, round):
    # Inisialisasi array kosong
    output = np.zeros((5,5,64), dtype = int) # ukuran sama dengan array input
    bit = np.zeros(dtype = int, shape = (5,5,64)) # akan menampung bit yang akan mengubah S
    kr = np.zeros(dtype = int, shape = 168) # akan menampung konstanta ronde

    # Menghitung Linear-Feedback Shift Register (LFSR)
    w = np.array([1,0,0,0,0,0,0,0], dtype = int)
    kr[0] = w[0]
    for i in range(1, 7*24):
        a = np.bitwise_xor(w[0], w[4])
        b = np.bitwise_xor(w[5], w[6])
        tail = np.bitwise_xor(a, b)
        w = [w[1],w[2],w[3],w[4],w[5],w[6],w[7], tail]
        kr[i] = w[0]
    # Menghitung bit yang akan mengubah S berdasarkan LFSR
    for l in range(7):
        q = pow(2, l) - 1
        t = l + 7*round
        bit[0][0][q] = kr[l + 7*round]
    # Menghitung output
    for i in range(5):
        for j in range(5):
            for k in range(64):
                output[i][j][k] = np.bitwise_xor(input[i][j][k], bit[i][j][k])
    return output

# Operasi pengubahan bentuk input dari string menjadi array biner
def toBinary(plain):
    num,two,res = [],[],[]
    for i in plain:
        num.append(ord(i))
    for j in num:
        two.append(bin(j)[2:])
    for k in two:
        if len(k) < 8:
            res.append('0')
        for l in k:
            res.append(l)
    return res

def addPad(arr, r):
    less = r - 1
    end = arr.size % r
    if end == 0:
        pad = np.zeros(r, dtype = int)
        pad[0] = 1
        pad[less] = 1
        arr = np.concatenate((arr, pad))
    elif end == less: 
        pad = np.zeros(r, dtype = int)
        arr = np.append(arr, 1)
        pad[less] = 1
        arr = np.concatenate((arr, pad))
    else:
        s = r - end
        pad = np.zeros(s, dtype = int)
        pad[0] = 1
        pad[s - 1] = 1
        arr = np.concatenate((arr, pad))
    return arr

# Algoritma SHA-3
def sha3(plain, cut):
    M = toBinary(plain)
    r = 1600 - 2*cut

    # Mengubah M menjadi np.array dan memberikan padding
    padded = np.array(M, dtype = int)
    padded = addPad(padded, r)

    # Inisiasi proses absorbsi
    P = []
    state = []
    n = padded.size // r
    P = np.split(padded, n)
    state = np.split(np.zeros(1600, dtype = int), [r])

    for i in range(n): # Untuk setiap partisi pesan berukuran r bit
        state[0] = np.bitwise_xor(state[0], P[i])

        # Melakukan proses terhadap state untuk 24 ronde
        temp = oneToThree(np.concatenate((state[0], state[1])))
        for rounds in range(24):
            temp = iota(chi(pi(rho(theta(temp)))), rounds)
        state = np.split(threeToOne(temp), [r])

    # Mengambil bagian r dari state (squeezing) lalu mengubahnya menjadi hexadecimal
    # Karena Keccak (SHA-3) 224, 256, 384, dan 512 bit semuanya selalu memiliki
    # ukuran blok r (rate) > ukuran d (digest) yang diinginkan, maka proses
    # squeezing hanya dilakukan sekali.
    Z = ''
    Z = Z + ''.join(format(x, '0x') for x in state[0][:cut]) 
    Z = hex(int(Z, 2))[2:]
    return Z

# Test drive
if __name__ == "__main__":
    print(sha3("halo", 256))