#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)


r = GMul(GMul(a, constant(1, 8)), constant(5, 8))

res = GMul(a, constant(5, 8))

checkResults(r, res)



