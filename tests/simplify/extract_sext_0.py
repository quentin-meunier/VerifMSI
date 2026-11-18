#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 8)
e = SignExt(24, p)
n = Extract(30, 23, e)

res = SignExt(7, Extract(7, 7, p))

checkResults(n, res)

