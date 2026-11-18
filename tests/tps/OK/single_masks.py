#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


m0 = symbol("m0", 'M', 1)
m1 = symbol("m1", 'M', 1)
m2 = symbol("m2", 'M', 1)

k = symbol("k", 'S', 1)

e = ((m2 & k) ^ m1) & ((~m0 ^ m1) ^ k)

checkTpsResult(e, True)

