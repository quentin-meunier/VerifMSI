#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'S', 8)

pb = getBitDecomposition(p)

for i in range(1000):

    v = random.randint(0, 256 - 1)
# std::cout << v << std::endl;

    c0 = constant(v, 8)

    n0 = pb + c0

# std::cout << "n0: " << n0 << std::endl;

    n1 = getBitDecomposition(n0)

# std::cout << "n1: " << n1 << std::endl;

    c1 = constant((256 - v) % 256, 8)

    n2 = n1 + c1

# std::cout << "n2: " << n2 << std::endl;

    n = getBitDecomposition(n2)

    if not equivalence(simplify(n), pb):

        print("KO: ", v)
        sys.exit(1)
print("OK")
sys.exit(0)
