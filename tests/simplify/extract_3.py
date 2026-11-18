#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
n0 = SignExt(24, k)
n1 = Extract(7, 0, n0)

checkResults(n1, k)

