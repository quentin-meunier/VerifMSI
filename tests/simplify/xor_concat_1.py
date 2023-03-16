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

n = Concat(a, b) ^ Concat(c, d) ^ Concat(e, f) ^ Concat(g, h)

wres = Concat(a ^ c ^ e ^ g, b ^ d ^ f ^ h)

checkResults(n, wres)

