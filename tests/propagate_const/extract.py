#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


c0 = constant(0x12345678, 32)

c = Extract(15, 8, c0)

res = constant(0x56, 8)

if equivalence(c, res):
    print('OK')
else:
    print('KO')


