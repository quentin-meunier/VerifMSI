#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


s = symbol("s", 'P', 16)

c = constant(0x1, 16)

e = s + c - s - c

n = LShR(s, e)

checkResults(n, n)

