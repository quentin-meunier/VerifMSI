#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)
u = symbol('u', 'P', 8)
v = symbol('v', 'P', 8)
z = symbol('z', 'P', 8)
w = symbol('w', 'P', 8)


r = GMul(a, GMul(u, (v ^ z)) ^ d) ^ GMul(a, d ^ GMul(u, (w ^ z)))


res = GMul(a, u, v ^ w)

checkResults(r, res)



