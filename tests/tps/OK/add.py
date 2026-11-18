#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k0 = symbol("k0", 'S', 8)

m = symbol("m", 'M', 8)

n = k0 + m
print("# Mask Occ in node: ", n)
n.printMaskOcc()

checkTpsResult(n, True)

