#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'S', 4)

pb = getBitDecomposition(p)

n0 = -p

# std::cout << "n0: " << n0 << std::endl;

n1 = -n0

print("n1: ", n1)

n = getBitDecomposition(n1)

# std::cout << "n: " << n << std::endl;

checkResults(n, getBitDecomposition(p))

