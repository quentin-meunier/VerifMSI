#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


p = symbol("p", 'P', 2)
q = symbol("q", 'P', 2)

n = -p + q

res = q - p

checkResults(n, res)

