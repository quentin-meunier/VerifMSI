#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k = symbol("k", 'S', 8)
m = symbol("m", 'M', 8)
u = getRealShares(k, 3)

u0 = u[0]
u1 = u[1]

usedBitExp = False
outIdx = {0}

# u0 uses share index 0 (in outIdx), so 0 additional input shares are needed -> PINI with maxShareOcc = 0
res1 = checkPINIVal(u0 ^ m, 0, outIdx, usedBitExp)
# u0 ^ u1 uses share index 1 (not in outIdx), so fails for maxShareOcc = 0
res2 = checkPINIVal(u0 ^ u1, 0, outIdx, usedBitExp)

if res1 and not res2:
    print("OK")
else:
    print("KO")

