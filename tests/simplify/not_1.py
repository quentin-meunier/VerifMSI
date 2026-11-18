#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# &       &
# |       |
# ~   ->  |
# |       |
# ~       |
# |       |
# k       k

k0 = symbol("k0", 'S', 8)

n0 = ~k0
n = ~n0

res = k0

checkResults(n, res)

