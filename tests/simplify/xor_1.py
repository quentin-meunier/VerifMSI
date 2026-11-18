#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# k0 ^ k0 ^ m0
m0 = symbol("m0", 'M', 8)
k0 = symbol("k0", 'S', 8)

n0 = k0 ^ m0
n = n0 ^ k0

checkResults(n, m0)

