#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# m0 ^ m0
m0 = symbol("m0", 'M', 8)
n = m0 ^ m0

# result is 0
res = constant(0, 8)

checkResults(n, res)

