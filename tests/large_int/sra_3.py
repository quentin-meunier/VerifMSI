#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0xef, 8)
r = c0 >> 4
c1 = constant(0xfe, 8)

checkResults(r, c1)

