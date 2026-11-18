#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

c0 = constant(1, 8)
c1 = constant(5, 8)
c2 = constant(6, 8)

n0 = c0 + c1

checkResults(n0, c2)

n0.dump("graph.dot")


