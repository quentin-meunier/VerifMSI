#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'P', 2)
b = symbol("b", 'P', 2)
c = symbol("c", 'P', 2)
d = symbol("d", 'P', 2)
e = symbol("e", 'P', 2)
f = symbol("f", 'P', 2)
g = symbol("g", 'P', 2)

cst64 = constant(0xffffffffffffffff, 64)
n0 = simplify(Concat(cst64, cst64))

cst4 = constant(0xf, 4)
cst8 = constant(0xff, 8)
cst48 = constant(0xffffffffffff, 48)
cst112 = Concat(cst64, cst48)
n1 = Concat(cst4, a, cst8, b, cst112)

cst7 = constant(0x7f, 7)
cst5 = constant(0x1f, 5)
cst46 = constant(0x3fffffffffff, 46)
cst110 = Concat(cst64, cst46)
n2 = Concat(c, cst7, d, cst5, e, cst110)

n = n0 ^ n1 ^ n2

cst2 = constant(0x3, 2)
cst3 = constant(0x7, 3)
res = Concat(c, cst2, a, cst3, d, cst3, b, e, cst110)

checkResults(n, res)

