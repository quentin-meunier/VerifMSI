#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0xAA, 992)
c1 = constant(0x12345678, 32)
n = Concat(c0, c1)
ref = constant(0xAA12345678, 1024)

print("res: ", n)
print("ref: ", ref)

checkResults(n, ref)

