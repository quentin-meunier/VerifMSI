#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'S', 3)
q = symbol("q", 'S', 3)

pb = getBitDecomposition(p)

n0 = p + q

n1 = getBitDecomposition(n0)

# std::cout << "n1: " << n1 << std::endl;

n2 = -q
n3 = getBitDecomposition(n2)

# std::cout << "n3: " << n3 << std::endl;

n4 = n1 + n3
n = getBitDecomposition(n4)

# std::cout << "n: " << n << std::endl;

checkResults(n, pb)

