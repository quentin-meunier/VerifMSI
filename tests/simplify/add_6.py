#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

c0 = constant(-2, 8)
c1 = constant(2, 8)
k0 = symbol("k0", 'S', 8)

n0 = c0 + c1
n1 = k0 | n0

checkResults(n1, k0)


