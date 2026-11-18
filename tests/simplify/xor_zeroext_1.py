#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)

n = ZeroExt(24, k) ^ ZeroExt(24, k) ^ ZeroExt(24, constant(12, 8))

res = constant(12, 32)

checkResults(n, res)

