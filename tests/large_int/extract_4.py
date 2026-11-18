#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x5555555555555555, 64)
c1 = Concat(c0, c0)
n = Extract(127, 0, c1)

print("res: ", n)
print("ref: ", c1)

checkResults(n, c1)

