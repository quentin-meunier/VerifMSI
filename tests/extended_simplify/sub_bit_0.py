#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'S', 4)

n0 = getBitDecomposition(-p)

# std::cout << "n0: " << n0 << std::endl;

n1 = -n0

# std::cout << "n1: " << n1 << std::endl;

n = getBitDecomposition(n1)

# std::cout << "n: " << n << std::endl;

checkResults(n, getBitDecomposition(p))

