#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0xFFFFFFFF, 32)
c1 = constant(0xF, 32)

n = c0 * c1
res = constant(0xFFFFFFF1, 32)

checkResults(n, res)

c2 = constant(0xFFFFFFFFFFFFFFFF, 64)
c3 = constant(0xF, 64)
n2 = c2 * c3
res2 = constant(0xFFFFFFFFFFFFFFF1, 64)

checkResults(n2, res2)

