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

'''
Unencrypted data: The quick brown fox rapped about some lazy bitch
Encrypted data: b'\xda5\x1a\xb7\xa9\xf8\xe7\x0e\xc0\x83N6;d\xd1e4V\xa6\xeb@\x8f\xc39\x04P0e\xcb\x02\xcc}A\xc2\xe2\xe2:\xd9\x80\xf4MVo\xa7\x7f\xe2&?'
Decrypted data: The quick brown fox rapped about some lazy bitch

iv: b'b\x8f\x9d-C\x00d\x11\xaf\xd4\xe3\xde4+\x82u' salt: b"z\\\xde^\x9b\xb1\xd2\x99\x1a'\xfd\xdb0\xe6\x93UP-\xb4\xb4\x89\x05^\x04\x9aF\x87\xd0\xd4\x1a\xcd\x9b" key: b'\xaazS\x94\xa2\xe6r\x13E\x0c\xf1\xed(\xba\x0e~Y\x08\xe13_\xeb\xa1\xf9r\xc8\t\x80F\xc2\xe9Q' newkey: b'\xaazS\x94\xa2\xe6r\x13E\x0c\xf1\xed(\xba\x0e~Y\x08\xe13_\xeb\xa1\xf9r\xc8\t\x80F\xc2\xe9Q'

Unencrypted data: The quick brown fox rapped about some lazy
Unecrypted hexed data: b'54686520717569636b2062726f776e20666f78207261707065642061626f757420736f6d65206c617a7920'
Pad length: 5
0505050505
Padded unecrypted hexed data: b'54686520717569636b2062726f776e20666f78207261707065642061626f757420736f6d65206c617a79200505050505'
Encrypted data: b'\x9b\xea\xb5\xe6\n\x0bo\x1a\x8c\xaa\xf2\xd5\x90\x02f\x04q\x7f\\\x13\xa7.L\xe3\xe8ki\xdd\xee\x17r\xa2\xceh\x93\x9ay\xf4\x85\xa1\xb6\xa7\xbb\xc8\xa8\xd7*\xea'
Decrypted data: The quick brown fox rapped about some lazy

iv: b'S\xae\x01\xbc+\xe9\x82(9\x1b\xf20\xa0\xf8*>' salt: b'\xca\xb2\xecT\xedc\xef\x92\xee\x90\xe94Gy\x9d\x1b\xd9\xaa\x8bv\x88\xdeM9\xa22\xbc\xb5\xd6c\r\xba' key: b'\xb1s\x90\t\xe0\x1bm\x9e\xbeo\x82{|\xe6\x0b6\x849\x8b\x10y\x8a\x01\x06Z\x91h\x7fi8\xbbP' newkey: b'\xb1s\x90\t\xe0\x1bm\x9e\xbeo\x82{|\xe6\x0b6\x849\x8b\x10y\x8a\x01\x06Z\x91h\x7fi8\xbbP'
'''

password = 'superman'
salt = b'\xca\xb2\xecT\xedc\xef\x92\xee\x90\xe94Gy\x9d\x1b\xd9\xaa\x8bv\x88\xdeM9\xa22\xbc\xb5\xd6c\r\xba'
iv = b'S\xae\x01\xbc+\xe9\x82(9\x1b\xf20\xa0\xf8*>'

key = EVP.pbkdf2(password, salt, 1000, 32)

print "key:",hexlify(key)

print "realkey:",hexlify(b'\xaazS\x94\xa2\xe6r\x13E\x0c\xf1\xed(\xba\x0e~Y\x08\xe13_\xeb\xa1\xf9r\xc8\t\x80F\xc2\xe9Q')

#c_data = b'\xda5\x1a\xb7\xa9\xf8\xe7\x0e\xc0\x83N6;d\xd1e4V\xa6\xeb@\x8f\xc39\x04P0e\xcb\x02\xcc}A\xc2\xe2\xe2:\xd9\x80\xf4MVo\xa7\x7f\xe2&?'
c_data = b'\x9b\xea\xb5\xe6\n\x0bo\x1a\x8c\xaa\xf2\xd5\x90\x02f\x04q\x7f\\\x13\xa7.L\xe3\xe8ki\xdd\xee\x17r\xa2\xceh\x93\x9ay\xf4\x85\xa1\xb6\xa7\xbb\xc8\xa8\xd7*\xea'
#c_data = unhexlify('da351ab7a9f8e70ec0834e363b64d1653456a6eb408fc33904503065cb02cc7d41c2e2e23ad980f44d566fa77fe2263f252b14518cefc9da7261bd1ba12f11b6')
#p_data = unhexlify('54686520717569636b2062726f776e20666f78207261707065642061626f757420736f6d65206c617a7920626974636810101010101010101010101010101010')

# By default in m2, padding is True. The result is the ciphered and plaintext data above.
# Were the actual c_data in hex, it would be the same as the commented c_data, but without
# the 10101010101010101010101010101010 (16 in hex to represent 16 bytes for 16 bytes)

cobj = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=0, key_as_bytes=False, padding=True)

pbuf = cStringIO.StringIO()
cbuf = cStringIO.StringIO(c_data)

p_data = cipher_filter(cobj, cbuf, pbuf)

pbuf.close()
cbuf.close()

print "original cipher:",hexlify(c_data)
print "decoded cipher:",p_data

#p_data = 'The quick brown fox rapped about some lazy '
cobj = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=1, key_as_bytes=False, padding=True)
pbuf = cStringIO.StringIO(p_data)
cbuf = cStringIO.StringIO()
new_data = hexlify(cipher_filter(cobj, pbuf, cbuf))
#new_data_padding = c_data[len(p_data) * 2:]
#new_data = new_data[:len(p_data) *2]

pbuf.close()
cbuf.close()

print "re-hexed cipher:",new_data

'''
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

c_data_padding = c_data[len(data) * 2:]

c_data = c_data[:len(data) *2]

pbuf.close()
cbuf.close()

print c_data

cobj = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=0) # 0 = dec

pbuf = cStringIO.StringIO()
cbuf = cStringIO.StringIO(unhexlify(c_data + c_data_padding))

p_data = cipher_filter(cobj, cbuf, pbuf)

pbuf.close()
cbuf.close()

print p_data
'''
