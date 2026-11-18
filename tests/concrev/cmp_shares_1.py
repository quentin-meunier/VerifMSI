#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)

shares = getRealShares(k, 3)
a0 = shares[0]
a1 = shares[1]
a2 = shares[2]

e0 = a0 ^ a1 ^ constant(0x34, 8) ^ a2
e1 = k ^ constant(0x34, 8)


r = compareExpsWithRandev(e0, e1, 100)

if r:
    print("OK")
else:
    print("KO")

r = compareExpsWithExev(e0, e1)

if r:
    print("OK")
else:
    print("KO")


be0 = getBitDecomposition(e0)
be1 = getBitDecomposition(e1)

r = compareExpsWithRandev(be0, be1, 100)

if r:
    print("OK")
else:
    print("KO")

r = compareExpsWithExev(be0, be1)

if r:
    print("OK")
else:
    print("KO")


