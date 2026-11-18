#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'P', 8)
q = symbol("q", 'P', 8)

c0 = constant(0xFF, 8)
c1 = constant(0xFF, 8)
c2 = constant(0xFF, 8)

n = c0 & p & c1 & q & c2

res = p & q

checkResults(n, res)

