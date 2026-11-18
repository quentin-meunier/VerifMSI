#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)

n = GMul(a, a, a, a)

res = GPow(a, constant(4, 8))

checkResults(n, res)

