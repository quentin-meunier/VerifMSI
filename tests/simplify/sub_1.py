#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 2)
c = constant(0, 2)

n = k - k
# result is k
res = c


checkResults(n, res)

