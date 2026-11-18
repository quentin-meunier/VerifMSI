#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

c0 = constant(0x1111111111111111, 64)
c1 = constant(0x2222222222222222, 64)
n = Concat(c1, c0)

# 1. Logical shift right by exact multiple of 64 (LShR by 64)
r64 = LShR(n, 64)
ref64 = Concat(constant(0, 64), c1)
checkResults(r64, ref64)

# 2. Logical shift right on non-multiple of 64 width (100 bits, LShR by 64)
n100 = Concat(constant(0xABCDE1234, 36), constant(0x1111111111111111, 64))
r100 = LShR(n100, 64)
ref100 = Concat(constant(0, 36), constant(0x0000000ABCDE1234, 64))
checkResults(r100, ref100)

