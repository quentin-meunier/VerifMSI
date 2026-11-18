#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# root       root
# ^          1
# /|\   ->
# m 1 m


k0 = symbol("k0", 'S', 8)

c0 = constant(255, 8)

n = k0 ^ c0 ^ k0

res = c0


checkResults(n, res)

