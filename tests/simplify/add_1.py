#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k0 = symbol("k0", 'S', 8)
c0 = constant(0, 8)

n0 = c0 + k0

checkResults(n0, k0)

n0.dump("graph.dot")


