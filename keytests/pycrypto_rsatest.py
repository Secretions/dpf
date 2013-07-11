#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

data = "some data"

rsa_1 = RSA.generate(2048)
rsa_1_pubkey = rsa_1.publickey()
print("Key #1:\n",rsa_1.exportKey())
print("Public Key #1:\n",rsa_1_pubkey.exportKey())

rsa_2 = RSA.generate(2048)
rsa_2_pubkey = rsa_2.publickey()
print("Key #2:\n",rsa_2.exportKey())
print("Public Key #2:\n",rsa_2_pubkey.exportKey())

rsa_3 = RSA.generate(2048)
rsa_3_pubkey = rsa_3.publickey()
print("Key #3:\n",rsa_3.exportKey())
print("Public Key #3:\n",rsa_3_pubkey.exportKey())

# Encrypt data for 1 and 2, but not 3
ciphertext = []
cipher = PKCS1_OAEP.new(rsa_1_pubkey)
ciphertext.append(cipher.encrypt(data.encode()))
cipher = PKCS1_OAEP.new(rsa_2_pubkey)
ciphertext.append(cipher.encrypt(bytes(data, 'utf-8'))) # alternate encode/decode

print(ciphertext)

cipher = PKCS1_OAEP.new(rsa_1)
print(cipher.decrypt(ciphertext[0]).decode())
cipher = PKCS1_OAEP.new(rsa_2)
print(str(cipher.decrypt(ciphertext[1]), 'utf-8'))
try:
    cipher = PKCS1_OAEP.new(rsa_3)
    print(cipher.decrypt(ciphertext[0]).decode())
except:
    print("If you see this, rsa_3 couldn't decode the text meant for rsa_1. Hooray!")
