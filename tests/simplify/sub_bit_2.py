#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'S', 4)

pb = getBitDecomposition(p)

n = pb - pb

# std::cout << "n: " << n << std::endl;

res = constant(0, 4)

checkResults(n, res)

