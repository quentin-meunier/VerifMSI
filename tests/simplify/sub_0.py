#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 3)
c = constant(0, 3)

n = k - c
# result is k
res = k


checkResults(n, res)

