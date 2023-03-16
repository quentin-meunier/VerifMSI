#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)


r = OpNode('M', [a, a, a, a])


res = GPow(a, constant(4, 8))

checkResults(r, res)



