#!/usr/bin/env python3

import os
import math
from binascii import hexlify,unhexlify

from Crypto.Cipher import AES
from Crypto import Random

from pbkdf2 import PBKDF2

password = 'superman'
salt = os.urandom(32)
iterations = 1000
keylength = 32

key = PBKDF2(password, salt, iterations).read(keylength)

iv = Random.new().read(AES.block_size)

data = "The quick brown fox rapped about some lazy "
print("Unencrypted data:",data)

hexed_data = hexlify(data.encode('ascii'))
print("Unecrypted hexed data:",hexed_data)

pad_length = int(16 - ((len(hexed_data)/2) % 16))
print("Pad length:",pad_length)

padding = '{0:0=2x}'.format(pad_length) * pad_length
print(padding)

padded_hexed_data = str(hexed_data, 'utf-8') + padding

print("Padded unecrypted hexed data:",padded_hexed_data.encode())

cobj = AES.new(key, AES.MODE_CBC, iv)

c_data = cobj.encrypt(unhexlify(padded_hexed_data.encode()))

print("Encrypted data:", c_data)

newkey = PBKDF2(password, salt, iterations).read(keylength)

cobj2 = AES.new(newkey, AES.MODE_CBC, iv)

print("Decrypted data:", str(cobj2.decrypt(c_data), 'utf-8'))

print("\niv:",iv,"salt:",salt,"key:",key,"newkey:",newkey)
