#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

sbox_data = [0]
def dummy_func(idx):
    return idx
k = symbol("k", 'S', 8)
m = symbol("m", 'M', 8)
shares = getRealShares(k, 2)
registerArray("sbox", 8, 8, 0x1000, 256, dummy_func, sbox_data, 1)
g0 = inputGate(shares[0])
g1 = inputGate(shares[1])
gm = inputGate(m)
gx0 = xorGate(g0, gm)
gx1 = xorGate(g1, gm)
outputs = [gx0, gx1]
nbCheck = 0
leak = checkSecurity(1, False, NI, outputs, False, nbCheck, False)
assert(leak == 0)

# Test large constants (> 64 bits) caching via Concat, Extract, ZeroExt, SignExt
c0 = constant(0x123456789ABCDEF0, 64)
c1 = constant(0xFEDCBA9876543210, 64)
big1 = Concat(c1, c0)
big2 = Concat(c1, c0)
assert(big1 == big2)
bigExt = ZeroExt(64, c0)
bigSext = SignExt(64, c1)
subBig = Extract(95, 16, big1)
bigNeg = Const(-1, 128)
bigNeg2 = Const(-1, 128)
assert(bigNeg == bigNeg2)

assert(Node.nodeNum > 0)
assert(HWElement.nodeNum > 0)

verifMSICleanup()

assert(Node.nodeNum == 0)
assert(HWElement.nodeNum == 0)
assert(len(Node.symb2node) == 0)
assert(len(Node.cst2node) == 0)
assert(len(ArrayExp.allArrays) == 0)
assert(len(HWElement.allHWElements) == 0)

# Re-create symbols, shares, and arrays with the exact same names after cleanup
k2 = symbol("k", 'S', 8)
m2 = symbol("m", 'M', 8)
shares2 = getRealShares(k2, 2)
registerArray("sbox", 8, 8, 0x1000, 256, dummy_func, sbox_data, 1)

e = (k2 ^ m2) ^ m2
checkResults(e, k2)

verifMSICleanup()

