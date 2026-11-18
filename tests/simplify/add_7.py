#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k = symbol("k", 'S', 8)
t = constant(0, 8)
p = constant(0, 8)

n0 = (k ^ t)
n = n0 + p

checkResults(n, k)


