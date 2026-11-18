#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


s = symbol("s", 'P', 16)

c = constant(0x1, 16)

e1 = s + c - s
e2 = LShR(LShR(s, c), e1)

# std::cout << "e2: " << e2.verbatimPrint() << std::endl;

r = LShR(s, constant(0x2, 16))

checkResults(e2, r)

