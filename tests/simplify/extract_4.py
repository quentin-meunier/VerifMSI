#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
n0 = ZeroExt(24, k)
n1 = Extract(7, 7, n0)

n2 = Extract(7, 7, k)

checkResults(n1, n2)

