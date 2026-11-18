#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


s = symbol("p", 'P', 4)

c = constant(0xffff, 16)

e = LShR(c, s)

res = Concat(LShR(constant(0x7fff, 15), s), constant(1, 1))

checkResults(e, res)

