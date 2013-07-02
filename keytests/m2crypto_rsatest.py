#!/usr/bin/env python

import os
import cStringIO
from M2Crypto import RSA, BIO
from binascii import hexlify, unhexlify

def gen_callback(*args):
    pass

data = "some data"

rsa_1 = RSA.gen_key(1024, 65537, callback=gen_callback)

bio_pub1 = BIO.MemoryBuffer()
rsa_1.save_pub_key_bio(bio_pub1)

print bio_pub1.read()
print rsa_1.as_pem(cipher='aes_256_cbc')

rsa_2 = RSA.gen_key(1024, 65537, callback=gen_callback)

bio_pub2 = BIO.MemoryBuffer()
rsa_2.save_pub_key_bio(bio_pub2)

rsa_2_pub = RSA.load_pub_key_bio(bio_pub2)

rsa_3 = RSA.gen_key(1024, 65537, callback=gen_callback)

bio_pub3 = BIO.MemoryBuffer()
rsa_3.save_pub_key_bio(bio_pub3)

padding = 'pkcs1_padding'

p = getattr(RSA, padding)
ctxt = rsa_2_pub.public_encrypt(data, p)

print hexlify(ctxt)

print rsa_2.private_decrypt(ctxt, p)
