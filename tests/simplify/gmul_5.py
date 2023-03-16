#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)

z = symbol('z', 'P', 8)


r = GMul(a, z) ^ GMul(z, (a ^ b)) ^ c


res = GMul(z, b) ^ c

checkResults(r, res)



