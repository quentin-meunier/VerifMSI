#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# 1. Arithmetic shift right by exact multiple of 64 (>> 64) on 92-bit negative constant
c0 = constant(0x11111111, 32)
c1 = constant(0x22222222, 32)
c2 = constant(0x08444444, 28)
n92 = Concat(c2, c1, c0)
r64 = n92 >> 64
ref64 = Concat(constant(0x0FFFFFFF, 28), constant(0xFFFFFFFFF8444444, 64))
checkResults(r64, ref64)

# 2. Arithmetic shift right by 64 on 128-bit negative constant
n128 = Concat(constant(0x8000000000000001, 64), constant(0x123456789ABCDEF0, 64))
r128 = n128 >> 64
ref128 = Concat(constant(0xFFFFFFFFFFFFFFFF, 64), constant(0x8000000000000001, 64))
checkResults(r128, ref128)

