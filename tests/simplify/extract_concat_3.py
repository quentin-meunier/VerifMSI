#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'S', 9)
b = symbol("b", 'S', 7)
c = symbol("c", 'S', 10)
d = symbol("d", 'S', 6)
n0 = Concat(d, c, b, a)

n = Extract(15, 0, n0)
res = Concat(b, a)

checkResults(n, res)

