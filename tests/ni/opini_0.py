#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'S', 1)
b = symbol("b", 'S', 1)
m = symbol("m", 'M', 1)

ua = getRealShares(a, 2)
ub = getRealShares(b, 2)

a0 = ua[0]
a1 = ua[1]
b0 = ub[0]

usedBitExp = False
outIdx = {0}
outLeaks = [[a0 ^ m, a1 ^ m]]

res1 = checkOPINIVal(a0 & b0, 0, outIdx, outLeaks, usedBitExp)
res2 = checkOPINIVal(a0 ^ a1, 0, outIdx, outLeaks, usedBitExp)

if res1 and not res2:
    print("OK")
else:
    print("KO")

