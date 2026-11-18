#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 32)

n0 = k ^ k
n1 = k ^ k

if equivalence(n0, n1):
    print("OK")
else:
    print("KO")

