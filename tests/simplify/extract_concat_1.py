#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
c = constant(0, 7)
d = constant(0, 10)
n0 = Concat(d, c, k, c)

n1 = Extract(14, 7, n0)

checkResults(n1, k)

