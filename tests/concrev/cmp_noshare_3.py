#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


m = symbol("m", 'M', 8)

e0 = Concat((m + m) << 1 ^ m & (-m + ~m), ZeroExt(7, Extract(0, 0, m)), SignExt(7, Extract(1, 1, m)), m >> 1, LShR(m, 2))
e1 = simplify(e0)

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


