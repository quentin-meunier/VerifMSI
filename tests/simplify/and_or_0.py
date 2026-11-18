#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

a = symbol("a", 'P', 8)
b = symbol("b", 'P', 8)
c = symbol("c", 'P', 8)
d = symbol("d", 'P', 8)
e = symbol("e", 'P', 8)

n = (~a & b) | (~a & ~b & c) | (~a & ~b & ~c & d) | (a + b + c) | (~a & ~b & ~c & ~d & e) | a
res = b | c | d | e | (a + b + c) | a

checkResults(n, res)

