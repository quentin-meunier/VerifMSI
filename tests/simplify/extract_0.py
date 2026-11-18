#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x12345678, 32)
c1 = constant(8, 8)
c2 = constant(15, 8)
n = Extract(c2, c1, c0)

res = constant(0x56, 8)

checkResults(n, res)

