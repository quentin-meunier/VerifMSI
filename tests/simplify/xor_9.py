#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# k ^ 1 ^ k actually is:
# ^
# / \
# ^   k
# / \
# k   1


# &          &
# \          \
# \     ->   \
# \          \
# ^          \
# /|\          \
# k 1  k         1


k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
c0 = constant(255, 8)

n0 = k0 ^ c0 ^ k0
n = n0 & k1

res = k1


checkResults(n, res)

