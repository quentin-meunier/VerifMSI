#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'S', 8)

pb = getBitDecomposition(p)

c0 = constant(0xff, 8)

n0 = pb + c0

# std::cout << "n0: " << n0 << std::endl;

n1 = getBitDecomposition(n0)

# std::cout << "n1: " << n1 << std::endl;

c1 = constant(1, 8)

n2 = n1 + c1

# std::cout << "n2: " << n2 << std::endl;

n = getBitDecomposition(n2)

checkResults(n, pb)

