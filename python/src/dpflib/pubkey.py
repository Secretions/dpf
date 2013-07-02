#!/usr/bin/env python

import dpflib

class rsa(object):
    'RSA Public Key Interface'

    def __init__(self, **kwargs):
        return self.init

    def init(self, **kwargs):
        self.debug = False
        self.length = 2048
        self.public_exponent = 65537
        self.debug = False
        self.rsa_key = False

        # blindly set args as values in object
        for arg,vaue in kwargs.items():
            setattr(self, arg, value)

    def gen_key():
        self.rsa_key = RSA.gen_key(self.length, self.public_exponent)
        print self.rsa_key
