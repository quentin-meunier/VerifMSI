#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# 1. Subtraction with borrow across 64-bit limb boundary (0x8000000000000000_0000000000000000 - 1)
a = Concat(constant(0x8000000000000000, 64), constant(0x0, 64))
b = constant(1, 128)
diff = a - b
ref = Concat(constant(0x7FFFFFFFFFFFFFFF, 64), constant(0xFFFFFFFFFFFFFFFF, 64))
checkResults(diff, ref)

# 2. Subtraction without borrow when low limb is 0xFFFFFFFFFFFFFFFF - 0
c = Concat(constant(0x0000000000000005, 64), constant(0xFFFFFFFFFFFFFFFF, 64))
d = Concat(constant(0x0000000000000002, 64), constant(0x0000000000000000, 64))
diff2 = c - d
ref2 = Concat(constant(0x0000000000000003, 64), constant(0xFFFFFFFFFFFFFFFF, 64))
checkResults(diff2, ref2)

# 3. Subtraction on non-multiple of 64 width (100 bits): 0 - 1 = (2^100 - 1)
z = constant(0, 100)
one = constant(1, 100)
diff3 = z - one
ref3 = Concat(constant(0xFFFFFFFFF, 36), constant(0xFFFFFFFFFFFFFFFF, 64))
checkResults(diff3, ref3)

