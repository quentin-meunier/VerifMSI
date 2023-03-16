#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)
z = symbol('z', 'P', 8)

e = GMul(GPow(x, y), GPow(x, z))

e = simplify(e)
res = GPow(x, y + z)

checkResults(e, res)






