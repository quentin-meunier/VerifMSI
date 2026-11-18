#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
shares = getRealShares(k, 2)
k0 = shares[0]
k1 = shares[1]
# std::cout << *k0.symb << std::endl;

e0 = k ^ k0
# std::cout << e0.verbatimPrint() << std::endl;

rud
sid = getDistribWithExev(replaceSharesWithSecretsAndMasks(e0), rud)

if rud and sid:
    print("OK")
else:
    print("KO")

e1 = k & k0

sid = getDistribWithExev(replaceSharesWithSecretsAndMasks(e1), rud)

if not rud and not sid:
    print("OK")
else:
    print("KO")


