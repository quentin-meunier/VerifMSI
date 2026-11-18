#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
k2 = symbol("k2", 'S', 8)
c0 = constant(255, 8)

# Node & n = c0 & k0 & k0 & c0 & c0 & k1 & c0 & k0 & k0 & k1 & k2 & c0 & k2 & c0 & k1 & k0 & c0
n0 = c0 & k0
n1 = n0 & k0
n2 = n1 & c0
n3 = n2 & c0
n4 = n3 & k1
n5 = n4 & c0
n6 = n5 & k0
n7 = n6 & k0
n8 = n7 & k1
n9 = n8 & k2
n10 = n9 & c0
n11 = n10 & k2
n12 = n11 & c0
n13 = n12 & k1
n14 = n13 & k0
n15 = n14 & c0

r0 = k0 & k1
res = r0 & k2

checkResults(n15, res)




