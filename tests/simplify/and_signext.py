#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k = symbol("k", 'S', 8)
p = symbol("p", 'P', 8)
m = symbol("m", 'M', 8)

n = SignExt(24, k) & SignExt(24, p) & SignExt(24, m)

res = SignExt(24, k & p & m)

checkResults(n, res)

