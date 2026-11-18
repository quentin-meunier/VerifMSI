#!/usr/bin/env python3
from verif_msi import *

m = symbol("m", 'M', 8)
e = m + m
e.printMaskOcc()

checkMaskOcc(
    e,
    None,
    {},
    {},
    {m: {e}}
)
