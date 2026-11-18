#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

m = symbol("m", 'M', 4)
n = symbol("n", 'M', 4)

p = symbol("p", 'P', 4)
q = symbol("q", 'P', 4)

k = symbol("k", 'S', 4)

rud
sid


e0 = k ^ m
sid = getDistribWithExev(e0, rud)

if rud and sid:
    print("OK")
else:
    print("KO")



e1 = k & m
sid = getDistribWithExev(e1, rud)

if not rud and not sid:
    print("OK")
else:
    print("KO")



e2 = k ^ p
sid = getDistribWithExev(e2, rud)

if not rud and not sid:
    print("OK")
else:
    print("KO")



e3 = p & (k ^ m)

sid = getDistribWithExev(e3, rud)
if not rud and sid:
    print("OK")
else:
    print("KO")



e4 = p | (k ^ m)

sid = getDistribWithExev(e4, rud)
if not rud and sid:
    print("OK")
else:
    print("KO")



e5 = m ^ p

sid = getDistribWithExev(e5, rud)
if rud and sid:
    print("OK")
else:
    print("KO")


e6 = m & p

sid = getDistribWithExev(e6, rud)
if not rud and sid:
    print("OK")
else:
    print("KO")



e7 = (m ^ p) & n

sid = getDistribWithExev(e7, rud)
if not rud and sid:
    print("OK")
else:
    print("KO")


e8 = (m ^ p) & q

sid = getDistribWithExev(e8, rud)
if not rud and sid:
    print("OK")
else:
    print("KO")

