#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'P', 8)
b = symbol("b", 'P', 2)
c = symbol("c", 'P', 8)
d = symbol("d", 'P', 2)
e = symbol("e", 'P', 4)
f = symbol("f", 'P', 4)
g = symbol("g", 'P', 6)

cst0 = constant(0xf, 4)
cst1 = constant(0xff, 8)
cst2 = constant(0x3, 2)
cst3 = constant(0x3f, 6)

n = Concat(cst0, a, cst0, b, cst3) ^ Concat(cst0, c, cst0, d, cst3) ^ Concat(e, cst1, f, cst2, g)

res = Concat(e, ~(a ^ c), f, ~(b ^ d), g)

checkResults(n, res)

