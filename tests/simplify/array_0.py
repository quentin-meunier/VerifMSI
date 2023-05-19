#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

p0 = symbol('p0', 'S', 3)
p1 = symbol('p1', 'S', 3)
p2 = symbol('p2', 'S', 3)
p3 = symbol('p3', 'S', 3)
a = ArrayExp('a', 3, 3, None, None, None, None)

f = p0 ^ p1 ^ p2 ^ p0
e = a[f]

res = a[p1 ^ p2]

checkResults(e, res)


