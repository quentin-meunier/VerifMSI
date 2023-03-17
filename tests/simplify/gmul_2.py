#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)


r = GMul(a, b, c) ^ GMul(a, b, d)

res = GMul(a, b, c ^ d)

checkResults(r, res)


