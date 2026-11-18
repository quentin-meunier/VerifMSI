#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

c0 = constant(0x1111111111111111, 64)
c1 = constant(0x2222222222222222, 64)
n = Concat(c1, c0)

# 1. Shift left by exact multiple of 64 (<< 64)
r64 = n << 64
ref64 = Concat(c0, constant(0, 64))
checkResults(r64, ref64)

# 2. Shift left across limb boundary on non-multiple of 64 width (100 bits, << 72)
n100 = Concat(constant(0x123456789, 36), constant(0xABCDEF0123456789, 64))
r72 = n100 << 72
ref72 = Concat(constant(0x345678900, 36), constant(0, 64))
checkResults(r72, ref72)

