#!/usr/bin/env python3
from verif_msi import *

m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)
k = symbol("k", 'S', 8)

n0 = m0 ^ k
n0.printMaskOcc()
checkMaskOcc(
    n0,
    None,
    {m0: n0},
    {m0: {n0: {n0: [1, 0]}}},
    {}
)

n1 = m1 + n0
n1.printMaskOcc()
checkMaskOcc(
    n1,
    None,
    {m0: n0, m1: n1},
    {
        m0: {n0: {n0: [1, 0], n1: [1, 1]}},
        m1: {n1: {n1: [1, 0]}}
    },
    {}
)

e = n1 + m0
e.printMaskOcc()
checkMaskOcc(
    e,
    None,
    {m1: n1},
    {
        m0: {n0: {n0: [1, 0], n1: [1, 1]}},
        m1: {n1: {n1: [1, 0], e: [1, 1]}}
    },
    {m0: {e}}
)
