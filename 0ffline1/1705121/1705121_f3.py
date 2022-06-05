#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:12:12 2022

@author: amanray
"""
import numpy
import numpy as np
import time
from BitVector import *

#import bitvector_demo

from collections import deque

import random
import math
import secrets
import random
import sys
sys.maxsize


from Cryptodome.Cipher import AES
from Crypto import Random 

def gcd(a, b):
        while b != 0:
            temp=a % b
            a=b
            b=temp
        return a

def multiplicativeInverse(a, b):
        x = 0
        y = 1
        lx = 1
        ly = 0
        oa = a 
        ob = b  
        while b != 0:
            q = a // b
            (a, b) = (b, a % b)
            (x, lx) = ((lx - (q * x)), x)
            (y, ly) = ((ly - (q * y)), y)
        if lx < 0:
            lx += ob  
        if ly < 0:
            ly += oa  
        return lx
def generatePrime(keysize):
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrime(num):
            return num
def isPrime(n):
    if n == 2:
        return True
    if not n & 1:
        return False
    return pow(2, n-1, n) == 1


def millerRabin(n, k):


    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True 

def KeyGeneration(size=8):
    
    #1)Generate 2 large random primes p,q (same size)
    p=generatePrime(size)
    q=generatePrime(size)
    if not (isPrime(p) and isPrime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #2)compute n=pq and phi=(p-1)(q-1)
    n = p * q
    phi = (p-1) * (q-1)

    #3) select random integer "e" (1<e<phi) such that gcd(e,phi)=1
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #4)Use Extended Euclid's Algorithm to compute another unique integer "d" (1<d<phi) such that e.d≡1(mod phi)
    d = multiplicativeInverse(e, phi)
    
    #5)Return public and private keys
    #Public key is (e, n) and private key is (d, n)
    return ((n, e), (d, n))

def encrypt(pk, plaintext):
    #1) obtain (n,e) 
    n, e = pk
    #2)message space [0,n-1]
    #3)compute c=m^e(mod n)
    c = [(ord(char) ** e) % n for char in plaintext]
    print(c)
    #4) send "C" to the other party
    return c

def decrypt(pk, ciphertext):
    d, n = pk
    #5)m=c^d (mod n)
    m = [chr((char ** d) % n) for char in ciphertext]
    return m


def encryptAES(cipherAESe,plainText):
    return cipherAESe.encrypt(plainText.encode("utf-8"))

def decryptAES(cipherAESd,cipherText):
    dec= cipherAESd.decrypt(cipherText).decode('utf-8')
    return dec
    




def main():
    pub,pri=KeyGeneration()

    
    key = secrets.token_hex(16)
   
    KeyAES=key.encode('utf-8')

    #3.	Encrypts the message under the data encapsulation scheme, using the symmetric key just generated.
    plainText = input("Enter the message: ")
    cipherAESe = AES.new(KeyAES,AES.MODE_GCM)
    nonce = cipherAESe.nonce
    print("Encrypting the message with AES......")
    cipherText=encryptAES(cipherAESe,plainText)
    print("AES cypher text: ")
    print(cipherText)


    #4.	Encrypt the symmetric key under the key encapsulation scheme, using Alice’s public key.
    cipherKey=encrypt(pub,key)
    print("Encrypting the AES symmetric key with RSA......")
    print("Encryted AES symmetric key cipherKey")
    print(cipherKey)
    #5.	Send both of these encryptions to Alice.
    #Sending.........
    
  #To decrypt this hybrid cipher-text, Alice does the following:

 #1.	Uses her private key to decrypt the symmetric key contained in the key encapsulation segment.
    decriptedKey=''.join(decrypt(pri,cipherKey))
    print("Decrypting the AES Symmetric Key...")
    print("AES Symmetric Key:")
    print(decriptedKey)

#2.	Uses this symmetric key to decrypt the message contained in the data encapsulation segment.
    decriptedKey=decriptedKey.encode('utf-8')
    cipherAESd = AES.new(decriptedKey, AES.MODE_GCM, nonce=nonce)
    decrypted=decryptAES(cipherAESd,cipherText)
    print("Decrypting the message using the AES symmetric key.....")
    print("decrypted message: ")
    print(decrypted)
    
    

    

if __name__ == "__main__":
    main()