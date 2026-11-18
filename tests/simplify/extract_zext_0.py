#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 8)
e = ZeroExt(24, p)

n = Extract(30, 23, e)

res = constant(0, 8)

checkResults(n, res)

