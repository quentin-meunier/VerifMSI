#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)
b = symbol("b", 'P', 8)
c = symbol("c", 'P', 8)
ab = a & b

n = OpNode('|', [ab, a, c])
res = a | c

checkResults(n, res)

