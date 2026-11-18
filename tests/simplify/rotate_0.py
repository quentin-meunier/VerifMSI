#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x12345678, 32)
n = RotateRight(c0, 8)

res = constant(0x78123456, 32)

checkResults(n, res)

