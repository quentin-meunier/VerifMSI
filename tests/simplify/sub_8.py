#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 2)
q = symbol("q", 'P', 2)
r = symbol("r", 'P', 2)

n = -p + q - r + p + (p - q) + r - p

res = constant(0, 2)

checkResults(n, res)

