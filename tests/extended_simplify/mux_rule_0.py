#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

x = symbol("x", 'P', 1)
y = symbol("y", 'P', 1)
p = symbol("p", 'P', 1)

e = (~p & x) ^ (p & y)


res = x ^ (p & (x ^ y))

checkResults(e, res)

