#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x78, 8)
c1 = constant(0x56, 8)
c2 = constant(0x34, 8)
c3 = constant(0x12, 8)
c4 = constant(0x12345678, 32)
n = Concat(c3, c2, c1, c0)

# result is 0x12345678
res = c4

checkResults(n, res)

