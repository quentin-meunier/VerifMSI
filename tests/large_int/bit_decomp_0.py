#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# 1. Bit decomposition of a 100-bit constant (64 + 36 bits, non-multiple of 64)
cHigh = constant(0x5A5A5A5A5, 36)
cLow = constant(0x123456789ABCDEF0, 64)
c100 = Concat(cHigh, cLow)
bd100 = getBitDecomposition(c100)
checkResults(bd100, c100)

# 2. Bit decomposition of a 65-bit constant (boundary 64 + 1 bits)
c65 = Concat(constant(1, 1), constant(0x8000000000000001, 64))
bd65 = getBitDecomposition(c65)
checkResults(bd65, c65)

# 3. Bit decomposition of a 130-bit constant (3 limbs: 64 + 64 + 2 bits)
c130 = Concat(
    constant(0x3, 2),
    constant(0xFEDCBA9876543210, 64),
    constant(0x0123456789ABCDEF, 64)
)
bd130 = getBitDecomposition(c130)
checkResults(bd130, c130)

