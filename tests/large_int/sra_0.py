#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0x11111111, 32)
c1 = constant(0x22222222, 32)
c2 = constant(0x33333333, 32)
c3 = constant(0x84444444, 32)
n = Concat(c3, c2, c1, c0)
r = n >> 72
ref = Concat(constant(0xFFFFFFFFFFFFFFFF, 64), constant(0xFF84444444333333, 64))

checkResults(r, ref)

