#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# root       root
# ^          ~
# /|\   ->    |
# 1            ^
# |\


k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

c0 = constant(255, 8)

n = k0 ^ k1 ^ c0

res0 = k0 ^ k1
res = ~res0


checkResults(n, res)

