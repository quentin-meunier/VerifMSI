#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("b", 'P', 16)
c0 = constant(0xffffffff, 32)
e1 = Concat(constant(0x1000, 13), p, constant(0x7, 3))
n = e1 & c0
res = Concat(constant(0x1000, 13), p, constant(0x7, 3))

checkResults(n, res)
