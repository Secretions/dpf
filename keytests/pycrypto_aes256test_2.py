#!/usr/bin/env python3

import os
import math
import re
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
print("Unencrypted data:",hexlify(data.encode()))

pad_length = 16 - len(data.encode('utf-8')) % 16
print("Pad length:",pad_length)

padding = '{0:0=2x}'.format(pad_length) * pad_length
print(padding)

padded_hexed_data = str(hexlify(data.encode()), 'utf-8') + padding

'''
### doesn't work because [0-9]x isn't programmable
def hexnum(num):
    base = 16
    last = 0
    for i in range(0,num):
        last = num + ((base*base)*last)
        print(hex(last))
    return last
print('{0:0=2x}'.format(hexnum(pad_length)))
padded_hexed_data = '{0:0=2x}'.format(hexnum(pad_length))
'''
print("Padded unecrypted hexed data:",padded_hexed_data.encode())

cobj = AES.new(key, AES.MODE_CBC, iv)

c_data = cobj.encrypt(unhexlify(padded_hexed_data.encode()))

print("Encrypted data:", c_data)

newkey = PBKDF2(password, salt, iterations).read(keylength)

cobj2 = AES.new(newkey, AES.MODE_CBC, iv)

decrypted_data = cobj2.decrypt(c_data)

pad_length_remove = -16

#print("Blah:",decrypted_data[-6])
for i in range(-1,-16,-1):
    if((i*-1) == decrypted_data[i]):
        print("Found padding:",i*-1)
        pad_length_remove = i
        break

print("Padding is:",pad_length_remove*-1)

# For giggles
#decrypted_data_str = re.sub(r'(.)\1+$', '', str(decrypted_data, 'utf-8'))
decrypted_data_str = str(decrypted_data[:pad_length_remove], 'utf-8')

print("Decrypted data:", hexlify(decrypted_data))
print("Decrypted depadded string:", decrypted_data_str)
print("Decrypted depadded string hexlified:", hexlify(decrypted_data_str.encode()))

print("\niv:",iv,"salt:",salt,"key:",key,"newkey:",newkey)
