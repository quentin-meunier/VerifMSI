#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 8)

n = (((p >> 1) >> 2) >> 3) + ((((p >> 1) >> 0) >> 3) >> 1)

res = (p >> 6) + (p >> 5)

checkResults(n, res)

