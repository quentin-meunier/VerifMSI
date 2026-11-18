#!/usr/bin/env python3
from verif_msi import *

m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)
k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

n0 = ~m0
n0.printMaskOcc()
checkMaskOcc(
    n0,
    [m0, n0],
    {},
    {},
    {m0: {n0}}
)

n1 = n0 ^ k0
n1.printMaskOcc()
checkMaskOcc(
    n1,
    None,
    {m0: n1},
    {m0: {n1: {n1: [1, 0]}}},
    {}
)

n2 = ~n1
n2.printMaskOcc()
checkMaskOcc(
    n2,
    None,
    {m0: n1},
    {m0: {n1: {n1: [1, 0], n2: [1, 1]}}},
    {}
)

n3 = m1 ^ n2
n3.printMaskOcc()
checkMaskOcc(
    n3,
    None,
    {m0: n1, m1: n3},
    {
        m0: {n1: {n1: [1, 0], n2: [1, 1], n3: [1, 2]}},
        m1: {n3: {n3: [1, 0]}}
    },
    {}
)

e = k1 ^ n3
e.printMaskOcc()
checkMaskOcc(
    e,
    None,
    {m0: n1, m1: n3},
    {
        m0: {n1: {n1: [1, 0], n2: [1, 1], n3: [1, 2], e: [1, 3]}},
        m1: {n3: {n3: [1, 0], e: [1, 1]}}
    },
    {}
)
