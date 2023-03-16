#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)

e = simplify(GExp(GLog(x)))

checkResults(e, x)




