#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
m = symbol("m", 'M', 8)
m0 = simplify(Extract(0, 0, m))

shares = getRealShares(k, 2)
k0 = shares[0]
k1 = shares[1]
k0b = getBitDecomposition(k0)
k1b = getBitDecomposition(k1)
k0b0 = simplify(Extract(0, 0, k0b))
k1b0 = simplify(Extract(0, 0, k1b))

kb = getBitDecomposition(k)
shares0 = getRealShares(simplify(Extract(0, 0, kb)), 2)
kb0 = shares0[0]
kb1 = shares0[1]

print("k    : ", k.verbatimPrint())
print("k0   : ", k0.verbatimPrint())
print("k0b  : ", k0b.verbatimPrint())
print("k1   : ", k1.verbatimPrint())
print("k1b  : ", k1b.verbatimPrint())
print("k0b0 : ", k0b0.verbatimPrint())
print("k1b0 : ", k1b0.verbatimPrint())
print("kb0  : ", kb0.verbatimPrint())
print("kb1  : ", kb1.verbatimPrint())


r = compareExpsWithRandev(k0b0 ^ m0, kb0 ^ m0, 100)

if r:
    print("OK")
else:
    print("KO")


r = compareExpsWithExev(k0b0 ^ m0, kb0 ^ m0)

if r:
    print("OK")
else:
    print("KO")


r = compareExpsWithRandev(k0b0, kb0, 100)

if r:
    print("OK")
else:
    print("KO")


r = compareExpsWithExev(k0b0, kb0)

if r:
    print("OK")
else:
    print("KO")


rud
sid = getDistribWithExev(replaceSharesWithSecretsAndMasks(k0b0), rud)
if rud and sid:
    print("OK")
else:
    print("KO")

sid = getDistribWithExev(replaceSharesWithSecretsAndMasks(kb0), rud)
if rud and sid:
    print("OK")
else:
    print("KO")

