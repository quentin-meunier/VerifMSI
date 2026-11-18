#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'P', 8)
c1 = constant(0x56, 8)
c2 = constant(0x34, 8)
c3 = constant(0x12, 8)
c4 = constant(0x123456, 24)
c5 = constant(0x563412, 24)

n = Concat(c3, c2, c1, a, c1, c2, c3, a, c3, c2, c1)
res = Concat(c4, a, c5, a, c4)

checkResults(n, res)

