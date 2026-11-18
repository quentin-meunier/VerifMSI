#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c = constant(0xFE, 8)
e = SignExt(55, c)
r = constant(0x7FFFFFFFFFFFFFFE, 63)

checkResults(e, r)


