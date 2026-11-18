#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

s0 = symbol("a", 'S', 32)
c8 = constant(0x99999999, 32)
c9 = constant(0x00000000, 32)
n0 = Concat(c9, c9, c9, c9, c9, c9, c9, c9, c9, c9)
r = getBitDecomposition(simplify(Concat(c9, n0, s0)))
n2 = Concat(c8, c8, c9, c9, c9, c9, c9, c9, c9, c9)
r2 = getBitDecomposition(simplify(Concat(c9, n2, c9)))

# std::cout << "r:  " << simplify(r).verbatimPrint() << std::endl;
# std::cout << "r2: " << simplify(r2).verbatimPrint() << std::endl;
# std::cout << "r | r2 : " << simplify(r2 | r).verbatimPrint() << std::endl;

n = r2 | r
res = getBitDecomposition(Concat(c9, n2, s0))

checkResults(n, res)

