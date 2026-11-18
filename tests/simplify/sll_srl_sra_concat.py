#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 8)
pb = getBitDecomposition(p)

n = LShR(((pb >> 1) << 2), 3)

e7 = simplify(Extract(7, 7, pb))
e6 = simplify(Extract(6, 6, pb))
e5 = simplify(Extract(5, 5, pb))
e4 = simplify(Extract(4, 4, pb))
e3 = simplify(Extract(3, 3, pb))
e2 = simplify(Extract(2, 2, pb))
e1 = simplify(Extract(1, 1, pb))
e0 = simplify(Extract(0, 0, pb))
res = Concat(constant(0, 1), constant(0, 1), constant(0, 1), e6, e5, e4, e3, e2)

checkResults(n, res)

