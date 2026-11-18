#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 4)
pb = getBitDecomposition(p)

n0 = Concat(pb, constant(0, 4))
n1 = simplify(n0 << 2)

e1 = simplify(Extract(1, 1, pb))
e0 = simplify(Extract(0, 0, pb))
res = Concat(e1, e0, constant(0, 6))

checkResults(n1, res, True)

