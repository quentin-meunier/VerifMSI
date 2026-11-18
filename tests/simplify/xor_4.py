#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# &          &
# \          \
# \     ->   ~
# \          \
# ^          ^
# /|\         |\
# 1


k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

c0 = constant(255, 8)

n0 = k0 ^ k1 ^ c0
n = n0 & k0

res0 = k0 ^ k1
res1 = ~res0
res = res1 & k0

checkResults(n, res)

