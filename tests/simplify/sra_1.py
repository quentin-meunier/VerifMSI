#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


c = constant(0xFFFFFFFFFFFFFFFF, 64)
e = c >> 8
r = constant(0xFFFFFFFFFFFFFFFF, 64)

checkResults(e, r)

