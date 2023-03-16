#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)

e = GMul(GExp(x), GExp(y))

e = simplify(e)
res = GExp(x + y)

checkResults(e, res)






