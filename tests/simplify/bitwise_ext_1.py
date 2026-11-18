#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k = symbol("k", 'S', 8)
p = symbol("p", 'P', 8)

n = Extract(7, 0, ZeroExt(24, k) ^ ZeroExt(24, p) ^ ZeroExt(24, k))

res = p

checkResults(n, res)

