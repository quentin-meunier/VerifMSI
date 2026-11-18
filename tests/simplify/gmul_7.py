#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)

n = GMul(GMul(a, constant(1, 8)), constant(5, 8))

res = GMul(a, constant(5, 8))

checkResults(n, res)

