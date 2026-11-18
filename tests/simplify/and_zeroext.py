#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k = symbol("k", 'S', 8)
p = symbol("p", 'P', 8)
m = symbol("m", 'M', 8)

n = ZeroExt(24, k) & ZeroExt(24, p) & ZeroExt(24, m)

res = ZeroExt(24, k & p & m)

checkResults(n, res)

