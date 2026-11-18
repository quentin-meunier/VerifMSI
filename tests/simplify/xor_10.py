#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# same as k9, but order of xor is different:
# matters because the xor is binary
# and k ^ k ^ 1 actually is:
# ^
# / \
# ^   1
# / \
# k   k

# &          &
# \          \
# \     ->   \
# \          \
# ^          \
# /|\          \
# k k 1          1


k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
c0 = constant(255, 8)

n0 = k0 ^ k0 ^ c0
n = n0 & k1

res = k1


checkResults(n, res)

