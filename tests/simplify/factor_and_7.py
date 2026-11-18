#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a0 = symbol("a0", 'P', 8)
a1 = symbol("a1", 'P', 8)
a2 = symbol("a2", 'P', 8)
b = symbol("b", 'P', 8)

n = ~(a0 | ~a1 | a2) | ((a0 | ~a1 | a2) & b)
res = ~(a0 | ~a1 | a2) | b

checkResults(n, res)

