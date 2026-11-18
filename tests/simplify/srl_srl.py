#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 8)

n = LShR(LShR(LShR(p, 1), 2), 3) + LShR(LShR(LShR(LShR(p, 1), 0), 3), 1)

res = LShR(p, 6) + LShR(p, 5)

checkResults(n, res)

