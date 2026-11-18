#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
c = constant(0, 7)
d = constant(0, 10)

n1 = Extract(7, 0, Concat(d, c, c, k))

checkResults(n1, k)

