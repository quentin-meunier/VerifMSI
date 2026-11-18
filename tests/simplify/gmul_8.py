#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)

n = GMul(GPow(a, constant(3, 8)), GPow(a, constant(2, 8)))

res = GPow(a, constant(5, 8))

checkResults(n, res)

