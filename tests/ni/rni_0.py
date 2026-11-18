#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k = symbol("k", 'S', 8)
m = symbol("m", 'M', 8)
u = getRealShares(k, 3)

u0 = u[0]
u1 = u[1]
u2 = u[2]

# 1. With 3 shares and diff = 1, combining 2 shares (u0 ^ u1) is 1-RNI if masked, not 2-RNI
usedBitExp = False
res1 = checkRNIVal(u0 ^ m, 2, usedBitExp)
res2 = checkRNIVal(u0 ^ u1 ^ u2, 1, usedBitExp)

if res1 and not res2:
    print("OK")
else:
    print("KO")

