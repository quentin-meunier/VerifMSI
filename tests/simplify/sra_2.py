#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


s = symbol("s", 'P', 16)

c = constant(0xffff, 16)

e = c >> s

checkResults(e, c)

