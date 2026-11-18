#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)
b = symbol("b", 'P', 8)
c = symbol("c", 'P', 8)
d = symbol("d", 'P', 8)
u = symbol("u", 'P', 8)
v = symbol("v", 'P', 8)
w = symbol("w", 'P', 8)
z = symbol("z", 'P', 8)

n = GMul(a, GMul(u, (v ^ z)) ^ d) ^ GMul(a, d ^ GMul(u, (w ^ z)))

res = GMul(a, u, v ^ w)

checkResults(n, res)

