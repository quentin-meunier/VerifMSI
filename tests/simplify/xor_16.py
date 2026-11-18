#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# (3 | (e ^ e)) ^ (4 | (f ^ f))

p = symbol("p", 'P', 4)
q = symbol("q", 'P', 4)

c0 = constant(15, 4)
c1 = constant(12, 4)

n = (c0 | (p ^ p)) ^ (c1 | (q ^ q))

res = constant(3, 4)


checkResults(n, res)

