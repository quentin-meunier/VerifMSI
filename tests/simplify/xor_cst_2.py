#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 8)
q = symbol("q", 'P', 8)

c0 = constant(0xA0, 8)
c1 = constant(0x0C, 8)
c2 = constant(0x03, 8)

n = (c0 ^ ~p ^ c1 ^ q ^ c2) & (c0 ^ p ^ c1 ^ q ^ c2)

res = (p ^ q ^ constant(0x50, 8)) & (p ^ q ^ constant(0xAF, 8))


checkResults(n, res)

