#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'P', 8)
b = symbol("b", 'P', 8)
c = symbol("c", 'P', 8)
d = symbol("d", 'P', 8)

n = Concat(a, Concat(Concat(d, b), c, Concat(Concat(a, b), b, Concat(c, d))), d, Concat(a, d))

res = Concat(a, d, b, c, a, b, b, c, d, d, a, d)

checkResults(n, res)

