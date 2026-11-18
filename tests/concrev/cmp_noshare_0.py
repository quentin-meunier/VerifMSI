#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


m0 = symbol("m0", 'M', 8)

e0 = Extract(Const(7, 3), Const(0, 1), (ZeroExt(Const(24, 5), m0) << Const(1, 1)))
e1 = Concat(Extract(6, 0, m0), Const(0, 1))

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


