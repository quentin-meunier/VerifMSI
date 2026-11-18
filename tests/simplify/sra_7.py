#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

e = constant(0x180000000, 33)
c = constant(31, 5)
y = symbol("y", 'P', 5)

n = e >> (c | y - y)
print("n : ", n)
s = simplify(n)
print("s : ", s)
r = constant(0x1ffffffff, 33)

checkResults(n, r)


