#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 3)
b = symbol('b', 'P', 7)
c = symbol('c', 'P', 3)
d = symbol('d', 'P', 7)
e = symbol('e', 'P', 3)
f = symbol('f', 'P', 7)
g = symbol('g', 'P', 3)
h = symbol('h', 'P', 7)

u = symbol('u', 'P', 10)
v = symbol('v', 'P', 10)
w = constant(0x93, 10)

n = u ^ Concat(a, b) ^ Concat(c, d) ^ v ^ Concat(e, f) ^ Concat(g, h) ^ w

res = Concat(a ^ c ^ e ^ g, b ^ d ^ f ^ h) ^ u ^ v ^ w

checkResults(n, res)

