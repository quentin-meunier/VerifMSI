#!/usr/bin/env python3
from verif_msi import *

m0 = symbol("m0", 'M', 8)

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

p0 = symbol("p0", 'P', 8)

n0 = m0 ^ k0
n1 = ~n0
n2 = n1 ^ k1
n3 = n2 + p0
e = n3 & n2

e.printMaskOcc()

checkMaskOcc(
    e,
    None,
    {},
    {
        m0: {n0: {n0: [2, 0], n1: [2, 1], n2: [2, 2], n3: [1, 3]}}
    },
    {}
)
