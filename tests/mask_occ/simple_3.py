#!/usr/bin/env python3
from verif_msi import *

m = symbol("m", 'M', 8)
k = symbol("k", 'S', 8)

n0 = k ^ m
n0.printMaskOcc()

checkMaskOcc(
    n0,
    None,
    {m: n0},
    {m: {n0: {n0: [1, 0]}}},
    {}
)

n1 = ~n0
n1.printMaskOcc()

checkMaskOcc(
    n1,
    None,
    {m: n0},
    {m: {n0: {n0: [1, 0], n1: [1, 1]}}},
    {}
)

e = n1 + n1
e.printMaskOcc()

checkMaskOcc(
    e,
    None,
    {},
    {m: {n0: {n0: [2, 0], n1: [2, 1]}}},
    {}
)
