#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)
m2 = symbol("m2", 'M', 8)
m3 = symbol("m3", 'M', 8)

n0 = k0 ^ m0 ^ m1
n1 = n0 & m2

n2 = m0 ^ m1 ^ k0
n3 = n2 & m2

n4 = n1 ^ n3 ^ m3
n5 = n4 + k1

for i in range(10):
    checkTpsResult(n5, True)



