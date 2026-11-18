#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 1)

m0 = symbol("m0", 'M', 1)

p0 = symbol("p0", 'P', 1)
p1 = symbol("p1", 'P', 1)
p2 = symbol("p2", 'P', 1)

n0 = k0 ^ m0

n1 = n0 & p0
n2 = ~n0
n3 = n0 | p2
n  = n1 + n2 + n3

checkTpsResult(n, True)

