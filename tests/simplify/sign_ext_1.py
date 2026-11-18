#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c = constant(0xFE, 8)
e = SignExt(56, c)
r = constant(0xFFFFFFFFFFFFFFFE, 64)

checkResults(e, r)


