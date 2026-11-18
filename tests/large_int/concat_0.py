#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x11111111, 32)
c1 = constant(0x22222222, 32)
n = Concat(c1, c0)

# result is 0x12345678
res = constant(0x2222222211111111, 64)

checkResults(n, res)

