#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)

r = a * b + a


res = a * (b + constant(0x01, 8))

checkResults(r, res)



