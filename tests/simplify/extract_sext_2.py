#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 1)
n = Extract(7, 0, SignExt(31, p))

res = SignExt(7, p)

checkResults(n, res)

