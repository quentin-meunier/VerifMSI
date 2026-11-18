#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# 0 ^ k0 ^ m0 ^ 0 ^ m1 ^ m2 ^ m0 ^ m1 ^ m0 ^ 0
k0 = symbol("k0", 'S', 8)
m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)
m2 = symbol("m2", 'M', 8)
c0 = constant(0, 8)

n = c0 ^ k0 ^ m0 ^ c0 ^ m1 ^ m2 ^ m0 ^ m1 ^ m0 ^ c0

res = k0 ^ m0 ^ m2

checkResults(n, res)

