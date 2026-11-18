#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)
k1 = symbol("k1", 'S', 8)

e0 = ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) & SignExt(Const(31, 5), Extract(Const(0, 1), Const(0, 1), ((((ZeroExt(Const(24, 5), (m1 ^ k1)) >> Const(1, 1)) >> Const(1, 1)) >> Const(1, 1)) >> Const(1, 1))))

e1 = ZeroExt(Const(24, 5), ((Concat(Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0)) & Const(27, 8)) ^ Concat(((Concat(Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0)) & Const(27, 7)) ^ Concat(((Concat(Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0)) & Const(27, 6)) ^ Concat(((Concat(Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 5)) ^ Concat(Extract(Const(3, 2), Const(0, 1), m0), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1)))) & SignExt(Const(31, 5), (Extract(Const(4, 3), Const(4, 3), m1) ^ Extract(Const(4, 3), Const(4, 3), k1)))


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


