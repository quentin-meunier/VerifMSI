#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k = symbol("k", 'S', 8)
n = Extract(7, 7, k >> 1)

res = Extract(7, 7, k)

checkResults(n, res)

