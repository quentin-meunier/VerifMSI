#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

m = symbol("m", 'M', 8)
n = symbol("n", 'M', 8)

e = (~(k0 ^ m) + k1) & n

checkTpsResult(e, True)

