#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)
b = symbol("b", 'P', 8)
c = symbol("c", 'P', 8)

n = GMul(a, b) ^ GMul(a, c)

res = GMul(a, (b ^ c))

checkResults(n, res)

