#!/usr/bin/env python3
from verif_msi import *

m = symbol("m", 'M', 8)
k = symbol("k", 'S', 8)
p = symbol("p", 'P', 8)

a = ArrayExp("a", 8, 8)

n0 = m ^ k
n1 = ~n0
n2 = a[n1]
n3 = OpNode('+', [p, n1, n2])
n4 = ~n1
n = OpNode('&', [n3, n2, n2, n1, n4])

n.printMaskOcc()

checkMaskOcc(
    n,
    None,
    {},
    {
        m: {n0: {n0: [6, 0], n1: [6, 1], n2: [3, 2], n4: [1, 2]}}
    },
    {}
)
