#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m = symbol("m", 'M', 8)

u = getPseudoShares(k0, 3)
v = getPseudoShares(k1, 3)

u0 = u[0]
u1 = u[1]
u2 = u[2]

v0 = v[0]
v1 = v[2]
v2 = v[2]

e0 = u0 ^ m ^ u1 ^ u2
# std::cout << "e0 : " << e0 << std::endl;
checkTpsResult(e0, True)

e1 = u0 ^ v0 ^ u1 ^ u2
checkTpsResult(e1, True)

