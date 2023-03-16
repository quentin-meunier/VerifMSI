#!/usr/bin/python

from verif_msi import *

a = symbol('a', 'S', 1)

a0, a1, a2, a3 = getRealShares(a, 4)

e0 = a0 ^ a1
e1 = a2 ^ a3

e2 = replaceSharesWithSecretsAndMasks(e0)
e3 = replaceSharesWithSecretsAndMasks(e1)

e = e2 ^ e3

e = simplify(e)

checkResults(e, a)

