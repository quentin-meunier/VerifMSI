#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
k2 = symbol("k2", 'S', 8)
c0 = constant(0, 8)
c1 = constant(255, 8)

n = c0 | k0 | k0 | c0 | c0 | k1 | c0 | k0 | k0 | k1 | k2 | c0 | k2 | c0 | k1 | k0 | c0 | c1

res = constant(255, 8)

checkResults(n, res)

