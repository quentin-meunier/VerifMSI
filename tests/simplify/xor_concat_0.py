#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'P', 3)
b = symbol("b", 'P', 7)
c = symbol("c", 'P', 11)
d = symbol("d", 'P', 5)
e = symbol("e", 'P', 3)
f = symbol("f", 'P', 7)
g = symbol("g", 'P', 11)
h = symbol("h", 'P', 5)

n = Concat(a, b, c, d) ^ Concat(e, f, g, h)

res = Concat(a ^ e, b ^ f, c ^ g, d ^ h)

checkResults(n, res)

