#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a0 = symbol("a0", 'P', 8)
a1 = symbol("a1", 'P', 8)
a2 = symbol("a2", 'P', 8)
a3 = symbol("a3", 'P', 8)
b = symbol("b", 'P', 8)
c = symbol("c", 'P', 8)

n = a0 | ~a1 | a2 | a3 | (b & c & ~(a0 | ~a1 | a2))
res = a0 | ~a1 | a2 | a3 | b & c

checkResults(n, res)

