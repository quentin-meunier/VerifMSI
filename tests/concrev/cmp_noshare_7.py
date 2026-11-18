#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


m = symbol("m", 'M', 8)

e0 = Concat(m, constant(0, 56)) + Concat(m, constant(0, 56))
e1 = constant(2, 64) * Concat(m, constant(0, 56))

r = compareExpsWithRandev(e0, e1, 10000)

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

r = compareExpsWithRandev(be0, be1, 10000)

if r:
    print("OK")
else:
    print("KO")

r = compareExpsWithExev(be0, be1)

if r:
    print("OK")
else:
    print("KO")


