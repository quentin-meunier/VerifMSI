#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 32)
k0 = Extract(15, 8, k)
p = symbol("P", 'P', 8)
n = k0 ^ p

n.dump("graph.dot")

