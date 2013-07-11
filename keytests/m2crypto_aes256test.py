#!/usr/bin/env python

import os
import cStringIO
from M2Crypto import EVP
from binascii import hexlify, unhexlify

#>>> EVP.pbkdf2('password', 'blah', iter=1000, keylen=32)

def cipher_filter(cipher, inf, outf):
    while 1:
        buf=inf.read()
        if not buf:
            break
        outf.write(cipher.update(buf))
    outf.write(cipher.final())
    return outf.getvalue()

password = 'superman'
salt = os.urandom(32)
iterations = 1000
keylength = 32

key = EVP.pbkdf2(password, salt, iterations, keylength)

iv = os.urandom(32)

data = "The quick brown fox rapped about some lazy bitch"

cobj = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=1) # 1 = enc

pbuf = cStringIO.StringIO(data)
cbuf = cStringIO.StringIO()

c_data = hexlify(cipher_filter(cobj, pbuf, cbuf))

print "raw data",c_data

c_data_padding = c_data[len(data) * 2:]

print "padding",c_data_padding

c_data = c_data[:len(data) *2]

print "final data",c_data

pbuf.close()
cbuf.close()

cobj = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=0) # 0 = dec

pbuf = cStringIO.StringIO()
cbuf = cStringIO.StringIO(unhexlify(c_data + c_data_padding))

p_data = cipher_filter(cobj, cbuf, pbuf)

pbuf.close()
cbuf.close()

print p_data
