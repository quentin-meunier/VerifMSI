#!/usr/bin/env python3
from verif_msi import *

m = symbol("m", 'M', 8)
n = ~m
n.printMaskOcc()

checkMaskOcc(
    n,
    [m, n],
    {},
    {},
    {m: {n}}
)

e = n + n
e.printMaskOcc()

checkMaskOcc(
    e,
    None,
    {},
    {},
    {m: {n}}
)
