#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
k2 = symbol("k2", 'S', 8)

# Node & n = k0 & k0 & k1 & k0 & k0 & k1 & k2 & k2 & k1 & k0;
n0 = k0 & k0
n1 = n0 & k1
n2 = n1 & k0
n3 = n2 & k0
n4 = n3 & k1
n5 = n4 & k2
n6 = n5 & k2
n7 = n6 & k1
n8 = n7 & k0

r0 = k0 & k1
res = r0 & k2

checkResults(n8, res)




