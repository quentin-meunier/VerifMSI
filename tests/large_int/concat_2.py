#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x111111, 24)
c1 = constant(0x22222222, 32)
c2 = constant(0x33333333, 32)
c3 = constant(0x4444444444, 40)
n = Concat(c3, c2, c1, c0)

print("res: ", n)
print("ref: 0x44444444443333333322222222111111")
if n.cst == 0x44444444443333333322222222111111:
    print("OK")
else:
    print("KO")

