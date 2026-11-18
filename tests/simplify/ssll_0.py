#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


s = symbol("p", 'P', 4)

c = constant(0xffff, 16)

e = c << s

res = Concat(constant(1, 1), constant(0x7fff, 15) << s)

checkResults(e, res)

