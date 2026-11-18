#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

e = constant(0x180000000, 33)
c = constant(31, 5)

n = LShR(e, c)
r = constant(0x3, 33)

checkResults(n, r)

