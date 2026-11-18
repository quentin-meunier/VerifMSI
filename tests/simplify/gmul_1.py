#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)
b = symbol("b", 'P', 8)

n = GMul(a, b) ^ a

res = GMul(a, (b ^ constant(0x01, 8)))

checkResults(n, res)

