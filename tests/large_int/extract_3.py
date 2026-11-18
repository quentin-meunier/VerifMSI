#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x5555555555555555, 64)
n = Extract(63, 0, c0)

print("res: ", n)
print("ref: 0x5555555555555555")
if n.cst == 0x5555555555555555:
    print("OK")
else:
    print("KO")

