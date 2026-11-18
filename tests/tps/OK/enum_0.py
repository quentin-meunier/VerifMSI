#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)

e0 = m0 ^ k0 | (m1 & k1)
# std::cout << "e0 : " << e0 << std::endl;
checkTpsResult(e0, False)

res
rud
res = getDistribWithExev(e0, rud)
print("# Res : ", res)

res = tpsNoFalsePositive(e0)
print("# Res : ", res)

