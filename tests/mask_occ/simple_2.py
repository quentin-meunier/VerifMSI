#!/usr/bin/env python3
from verif_msi import *

m = symbol("m", 'M', 8)
n0 = ~m
n1 = n0
n0.printMaskOcc()

checkMaskOcc(
    n0,
    [m, n0],
    {},
    {},
    {m: {n0}}
)

e = n0 + n1
e.printMaskOcc()

checkMaskOcc(
    e,
    None,
    {},
    {},
    {m: {n0}}
)
