#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# 1. ZeroExt from 36 bits to 100 bits
c36 = constant(0xABCDE1234, 36)
z100 = ZeroExt(64, c36)
refZ100 = Concat(constant(0, 64), c36)
checkResults(z100, refZ100)

# 2. SignExt of negative 36-bit constant to 100 bits
neg36 = constant(0x8BCDE1234, 36)
s100 = SignExt(64, neg36)
refS100 = Concat(constant(0xFFFFFFFFFFFFFFFF, 64), neg36)
checkResults(s100, refS100)

# 3. SignExt of positive 72-bit constant to 136 bits
pos72 = Concat(constant(0x7F, 8), constant(0x123456789ABCDEF0, 64))
s136 = SignExt(64, pos72)
refS136 = Concat(constant(0, 64), pos72)
checkResults(s136, refS136)

