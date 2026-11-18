#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m = symbol("m", 'M', 8)

u = getPseudoShares(k0, 3)
v = getPseudoShares(k1, 3)

a0 = u[0]
a1 = u[1]
a2 = u[2]

b0 = v[0]
b1 = v[2]
b2 = v[2]

e = a0 ^ a1 ^ b1 ^ b2

p = e | (a0 & b1)
checkTpsResult(p, True)

# std::cout << "e : " << e << std::endl;

f = (a2 ^ m ^ b0)
g = Concat(p, f)
checkTpsResult(g, True)

