#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0xFFFFFFFFFFFFFFFF, 64)
c1 = constant(0x7FFFFFFFFFFFFFFF, 64)
n0 = Concat(c1, c0)

n1 = constant(1, 128)
n = n0 + n1

# result is 0x80000000000000000000000000000000
res0 = constant(0x8000000000000000, 64)
res1 = constant(0x0000000000000000, 64)
res = Concat(res0, res1)

checkResults(n, res)

