#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# root       root
# ^          ~
# / \   ->    |
# m   1        m


k0 = symbol("k0", 'S', 8)
c0 = constant(0, 8)

n = k0 ^ k0

res = c0


checkResults(n, res)

