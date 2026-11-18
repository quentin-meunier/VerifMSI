#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x11111111, 32)
c1 = constant(0x22222222, 32)
c2 = constant(0x33333333, 32)
c3 = constant(0x44444444, 32)
n = Concat(c3, c2, c1, c0)
u = Extract(31, 0, n)
v = Extract(63, 32, n)
w = Extract(95, 64, n)
x = Extract(127, 96, n)

if equivalence(c0, u) and equivalence(c1, v) and equivalence(c2, w) and equivalence(c3, x):
    print("OK")
else:
    print("KO")

