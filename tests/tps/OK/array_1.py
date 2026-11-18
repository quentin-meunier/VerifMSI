#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

k = symbol("k", 'S', 3)
m = symbol("m", 'M', 3)
p = symbol("p", 'P', 3)

a = ArrayExp("a", 3, 3)

n = m ^ a[((k ^ m) << 1) ^ (m << 1) ^ p]

checkTpsResult(n, True)

