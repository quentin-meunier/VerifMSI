#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)

e = GPow(x, Const(16, 8)) ^ GPow(y, Const(16, 8))

e = simplify(e)
res = GPow(x ^ y, Const(16, 8))

checkResults(e, res)






