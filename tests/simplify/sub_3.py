#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c0 = constant(0, 8)
c1 = constant(0, 8)

n = c0 - c1
# result is 5
res = c0

checkResults(n, res)

