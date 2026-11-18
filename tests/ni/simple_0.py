#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m = symbol("m", 'M', 8)

u = getRealShares(k0, 3)
v = getRealShares(k1, 3)

u0 = u[0]
u1 = u[1]
u2 = u[2]

v0 = v[0]
v1 = v[1]
v2 = v[2]

e = u0 ^ m ^ u1 ^ u2
# std::cout << "e : " << e << std::endl;
checkNIResult(e, 2, True)

e2 = u0 ^ v0 ^ u1 ^ u2
checkNIResult(e2, 2, False)

