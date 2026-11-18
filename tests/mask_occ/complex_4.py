#!/usr/bin/env python3
from verif_msi import *

m0 = symbol("m0", 'M', 8)
k0 = symbol("k0", 'S', 8)
p0 = symbol("p0", 'P', 8)
p1 = symbol("p1", 'P', 8)

n0 = m0 ^ k0
n1 = ~n0
n4 = n0 & p0
n5 = n1 + n4
e = n5 + p1

e.printMaskOcc()

checkMaskOcc(
    e,
    None,
    {},
    {
        m0: {n0: {n0: [2, 0], n1: [1, 1]}}
    },
    {}
)
