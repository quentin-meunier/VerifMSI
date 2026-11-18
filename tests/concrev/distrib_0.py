#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

m0 = symbol("m0", 'M', 4)
m1 = symbol("m1", 'M', 4)
m2 = symbol("m2", 'M', 2)
k0 = symbol("k0", 'S', 4)

e0 = k0 ^ m0
rud
sid = getDistribWithExev(e0, rud)

if rud and sid:
    print("OK")
else:
    print("KO")


e1 = k0 & m0

sid = getDistribWithExev(e1, rud)
if not rud and not sid:
    print("OK")
else:
    print("KO")


e2 = k0 ^ m0 ^ m1

sid = getDistribWithExev(e2, rud)
if rud and sid:
    print("OK")
else:
    print("KO")


e3 = k0 ^ m0 ^ (ZeroExt(2, m2))

sid = getDistribWithExev(e3, rud)
if rud and sid:
    print("OK")
else:
    print("KO")


e4 = (k0 ^ m0) & m1

sid = getDistribWithExev(e4, rud)
if not rud and sid:
    print("OK")
else:
    print("KO")


# if using e0 instead of using a new alias, strange bug
e5 = k0

sid = getDistribWithExev(e5, rud)
if not rud and not sid:
    print("OK")
else:
    print("KO")

