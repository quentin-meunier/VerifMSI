#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# /        /
# ^        /
# / \   -> /
# ~a  1    a

k = symbol("k", 'S', 8)
p = symbol("p", 'S', 8)

c = constant(255, 8)

n0 = ~k ^ c
n = n0 & p

res = k & p


checkResults(n, res)

