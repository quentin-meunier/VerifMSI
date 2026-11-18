#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 8)
p0 = Extract(0, 0, p)

n = Extract(6, 0, Concat(p0, p0, p0, p0, p0, p0, p0, p0))
res = Concat(p0, p0, p0, p0, p0, p0, p0)

checkResults(n, res)

