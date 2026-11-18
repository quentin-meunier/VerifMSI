#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'P', 3)
b = symbol("b", 'P', 7)
c = symbol("c", 'P', 3)
d = symbol("d", 'P', 7)
e = symbol("e", 'P', 3)
f = symbol("f", 'P', 7)
g = symbol("g", 'P', 3)
h = symbol("h", 'P', 7)

n = Concat(a, b) ^ Concat(c, d) ^ Concat(e, f) ^ Concat(g, h)

res = Concat(a ^ c ^ e ^ g, b ^ d ^ f ^ h)


checkResults(n, res)

