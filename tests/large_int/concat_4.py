#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x5, 4)
c1 = constant(0x0, 60)
n = Concat(c0, c1)

print("res: ", n)
print("ref: 0x5000000000000000")
if n.cst == 0x5000000000000000:
    print("OK")
else:
    print("KO")

