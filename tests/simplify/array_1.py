#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p0 = symbol("p0", 'P', 3)
p1 = symbol("p1", 'P', 3)
p2 = symbol("p2", 'P', 3)
a = ArrayExp("a", 3, 3)

n = a[(p0 ^ p1) << 1 ^ (p1 << 1)]

res = a[p0 << 1]

checkResults(n, res, True)

