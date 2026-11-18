#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

p = symbol("p", 'S', 4)

pb = getBitDecomposition(p)
npb = getBitDecomposition(-p)

# std::cout << "pb :  " << pb << std::endl;
# std::cout << "npb:  " << npb << std::endl;

n = getBitDecomposition(pb + npb)

# std::cout << "n:    " << n << std::endl;

res = constant(0, 4)

checkResults(n, res)

