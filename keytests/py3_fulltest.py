#!/usr/bin/env python

import os
#import cStringIO
import io
from M2Crypto import EVP, RSA, BIO
from binascii import hexlify, unhexlify

### Straight from the m2crypto aes test
def cipher_filter(cipher, inf, outf):
    while 1:
        buf=inf.read()
        if not buf:
            break
        outf.write(cipher.update(buf))
    outf.write(cipher.final())
    return outf.getvalue()

### Generate example users w/keys
users = [RSA.gen_key(1024, 65537) for i in range(3)]

# Could save/load private keys via .as_pem, save_key, or save_key_bio
# use callback to provide custom passphrase stuff if needed

### user0 and user1 is recipient, user2 is nobody
recipient_pubkeys = [BIO.MemoryBuffer(), BIO.MemoryBuffer()]
users[0].save_pub_key_bio(recipient_pubkeys[0])
users[1].save_pub_key_bio(recipient_pubkeys[1])

# Create the key just for this encrypted password
one_time_key = os.urandom(32)
print('one time key {0}',hexlify(one_time_key))

# Encrypt the password w/key using aes-256-cbc
salt = os.urandom(32)
iterations = 10000
keylength = 32
key = EVP.pbkdf2(one_time_key, salt, iterations, keylength)

iv = os.urandom(32)

data = "Some_Password"

cipher_object = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=1) # 1 = enc
pbuf = io.BytesIO(data)
cbuf = io.BytesioIO()
hexed_cipher = hexlify(cipher_filter(cipher_object, pbuf, cbuf))
padded_hexed_cipher = hexed_cipher[:len(data) *2] + hexed_cipher[len(data) * 2:]
pbuf.close()
cbuf.close()

one_time_keys_encrypted = []
p = getattr(RSA, 'pkcs1_padding')

# encrypt one_time_key for all recipients
for recipient in recipient_pubkeys:
    pub = RSA.load_pub_key_bio(recipient)
    one_time_keys_encrypted.append(hexlify(pub.public_encrypt(one_time_key, p)))

new_key = []
# decrypt one time keys
for i in range(2):
    new_key.append(users[i].private_decrypt(unhexlify(one_time_keys_encrypted[i]), p))
    print('user',i,hexlify(new_key[i]))

try:
    print('user 0:',hexlify(users[0].private_decrypt(unhexlify(one_time_keys_encrypted[1]), p)))
except(Exception, e):
    print('User 1 using user 2 key should error:',e)
try:
    print('user 3:',hexlify(users[2].private_decrypt(unhexlify(one_time_keys_encrypted[0]), p)))
except(Exception, e):
    print('User 3 should error:',e)

### Decrypt password via one time key
for i in range(2):
    key = EVP.pbkdf2(new_key[i], salt, iterations, keylength)
    cipher_object = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=0) # 0 = dec
    pbuf = io.BytesIO()
    cbuf = io.BytesIO(unhexlify(padded_hexed_cipher))
    password = cipher_filter(cipher_object, cbuf, pbuf)
    print("user",i,password)
