#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)

e0 = k0 ^ m0

# TODO: trouver une expression qui ne fuit pas mais pour laquelle on ne conclut pas en symbolique

res
rud
res = getDistribWithExev(e0, rud)
print("# Res : ", res)

res = tpsNoFalsePositive(e0)
print("# Res : ", res)

