#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'P', 8)
m = symbol("m", 'M', 1)

n = Extract(7, 0, ZeroExt(24, p) ^ ZeroExt(31, m))

res = Concat(constant(0, 7), m) ^ p

checkResults(n, res)

