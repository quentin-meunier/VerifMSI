#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

c0 = constant(-2, 8)
c1 = constant(2, 8)
c2 = constant(4, 8)
c3 = constant(4, 8)
c4 = constant(0, 8)

k0 = symbol("k0", 'S', 8)

# n0 = (c0 + c1 + c2 + c3) ^ k0 ^ (c2 + c3) ^ k0
n0 = c0 + c1
n1 = n0 + c2
n2 = n1 + c3
n3 = n2 ^ k0
n4 = c2 + c3
n5 = n3 ^ n4
n = n5 ^ k0

checkResults(n, c4)




