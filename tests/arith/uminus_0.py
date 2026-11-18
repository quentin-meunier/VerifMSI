#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# 1. Unary minus on 0 (128 bits) -> 0
z = constant(0, 128)
checkResults(-z, z)

# 2. Unary minus when low limb is 0 and high limb is non-zero
a = Concat(constant(0x0000000000000001, 64), constant(0x0000000000000000, 64))
refA = Concat(constant(0xFFFFFFFFFFFFFFFF, 64), constant(0x0000000000000000, 64))
checkResults(-a, refA)

# 3. Unary minus on 100-bit constant (non-multiple of 64)
b = constant(1, 100)
refB = Concat(constant(0xFFFFFFFFF, 36), constant(0xFFFFFFFFFFFFFFFF, 64))
checkResults(-b, refB)

