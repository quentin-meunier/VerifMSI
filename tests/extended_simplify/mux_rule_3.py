#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

x = symbol("x", 'P', 1)
y = symbol("y", 'P', 1)
p = symbol("p", 'P', 1)
u = symbol("u", 'P', 1)
v = symbol("v", 'P', 1)
w = symbol("w", 'P', 1)
z = symbol("z", 'P', 1)

e = (~p & x) ^ u ^ v ^ w ^ z ^ (p & y)


res = x ^ (p & (x ^ y)) ^ u ^ v ^ w ^ z

checkResults(e, res)

