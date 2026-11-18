#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 32)
n = Extract(2, 1, Extract(15, 8, p))

res = Extract(10, 9, p)

checkResults(n, res)

