#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
k2 = symbol("k2", 'S', 8)

n = k0 | k0 | k1 | k0 | k0 | k1 | k2 | k2 | k1 | k0
res = k0 | k1 | k2

checkResults(n, res)

