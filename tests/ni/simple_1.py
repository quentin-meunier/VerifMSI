#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m = symbol("m", 'M', 8)

a = getRealShares(k0, 3)
b = getRealShares(k1, 3)

a0 = a[0]
a1 = a[1]
a2 = a[2]

b0 = b[0]
b1 = b[1]
b2 = b[2]

e = a0 ^ a1 ^ b1 ^ b2
checkNIResult(e, 2, True)

n = e | (a0 & b1)
checkNIResult(n, 2, True)

f = (a2 ^ m ^ b0)
g = Concat(n, f)
checkNIResult(g, 2, True)

