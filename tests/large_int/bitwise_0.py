#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

# 1. Bitwise NOT, AND, OR, XOR on 100-bit constants (width % 64 != 0)
a = Concat(constant(0x0F0F0F0F0, 36), constant(0xAAAAAAAAAAAAAAAA, 64))
b = Concat(constant(0xF0F0F0F0F, 36), constant(0x5555555555555555, 64))
allOnes = Concat(constant(0xFFFFFFFFF, 36), constant(0xFFFFFFFFFFFFFFFF, 64))
allZeros = constant(0, 100)

checkResults(~a, b)
checkResults(a ^ b, allOnes)
checkResults(a | b, allOnes)
checkResults(a & b, allZeros)

# 2. Simplification with isAllOne and isZero on > 64-bit symbols (65 bits)
s = symbol("s", 'S', 65)
ones65 = ~constant(0, 65)
zero65 = constant(0, 65)

checkResults(s & ones65, s)
checkResults(s | zero65, s)
checkResults(s ^ zero65, s)
checkResults(s ^ ones65, ~s)

