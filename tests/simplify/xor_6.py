#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# &          &
# \          \
# \     ->   \
# \          \
# ^          ~
# /|\         |
# 0 k 1        k

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
c0 = constant(0, 8)
c1 = constant(255, 8)

n0 = c0 ^ k0 ^ c1
n = n0 & k1

res0 = ~k0
res = res0 & k1


checkResults(n, res)

