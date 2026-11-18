#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# 1. Carry propagation when limb[1] has 0xFFFFFFFFFFFFFFFF + 0xFFFFFFFFFFFFFFFF + carry(1)
a0 = constant(0xFFFFFFFFFFFFFFFF, 64)
a1 = constant(0xFFFFFFFFFFFFFFFF, 64)
a2 = constant(0x0000000000000001, 64)
a = Concat(a2, a1, a0)

b0 = constant(0x0000000000000001, 64)
b1 = constant(0xFFFFFFFFFFFFFFFF, 64)
b2 = constant(0x0000000000000001, 64)
b = Concat(b2, b1, b0)

sum = a + b
ref = Concat(
    constant(0x0000000000000003, 64),
    constant(0xFFFFFFFFFFFFFFFF, 64),
    constant(0x0000000000000000, 64)
)
checkResults(sum, ref)

# 2. Non-multiple of 64 width (100 bits = 36 + 64) with overflow truncation on top limb
c0 = Concat(constant(0xFFFFFFFFF, 36), constant(0xFFFFFFFFFFFFFFFF, 64))
c1 = constant(2, 100)
sum2 = c0 + c1
ref2 = constant(1, 100)
checkResults(sum2, ref2)

