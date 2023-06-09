#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

p = symbol('p', 'P', 8)
q = symbol('q', 'P', 8)

c0 = constant(0xA0, 8)
c1 = constant(0x0A, 8)
c2 = constant(0xAA, 8)

n = c0 ^ p ^ c1 ^ q ^ c2

# result is 0
wres = p ^ q

checkResults(n, wres)


