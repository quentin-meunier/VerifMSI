#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x11111111, 32)
c1 = constant(0x22222222, 32)
c2 = constant(0x33333333, 32)
c3 = constant(0x44444444, 32)
n = Concat(c3, c2, c1, c0)
u = Extract(103, 16, n)
res = Concat(constant(0x44, 8), c2, c1, constant(0x1111, 16))

checkResults(u, res)

