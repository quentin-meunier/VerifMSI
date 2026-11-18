#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
n0 = ZeroExt(24, k)
n1 = Extract(15, 0, n0)

n2 = ZeroExt(8, k)

checkResults(n1, n2)

