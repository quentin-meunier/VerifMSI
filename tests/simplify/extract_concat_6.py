#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


a = symbol("a", 'S', 7)
b = symbol("b", 'S', 9)
c = symbol("c", 'S', 10)
d = symbol("d", 'S', 6)
n0 = Concat(d, c, b, a)

n = Extract(26, 7, n0)
res = Extract(19, 0, Concat(d, c, b))

checkResults(n, res)

