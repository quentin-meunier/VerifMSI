#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

m0 = symbol("m0", 'M', 2)
m1 = symbol("m1", 'M', 2)
m2 = symbol("m2", 'M', 2)
p0 = symbol("p0", 'P', 2)
p1 = symbol("p1", 'P', 2)
a = symbol("a", 'S', 2)
b = symbol("b", 'S', 2)
c = symbol("c", 'S', 2)

aShares = getRealShares(a, 4)
bShares = getRealShares(b, 4)
cShares = getRealShares(c, 4)

a0 = aShares[0]
a1 = aShares[1]
a2 = aShares[2]
a3 = aShares[3]

b0 = bShares[0]
b1 = bShares[1]
b2 = bShares[2]
b3 = bShares[3]

c0 = cShares[0]
c1 = cShares[1]
c2 = cShares[2]
c3 = cShares[3]

res

e0 = (a0 ^ a1 ^ b0) & p0 & (c0 ^ c1 ^ b0)
res = isNIWithExev(e0, 2)

if res:
    print("OK")
else:
    print("KO")

e1 = (a0 ^ a1 ^ b0) & p0 & (c0 ^ c1 ^ b0) & (a0 ^ a1 ^ a2 ^ m0)
res = isNIWithExev(e1, 2)

if res:
    print("OK")
else:
    print("KO")


