#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)


#n0 = (a & b) | a | c
n0 = OpNode('|', [a & b, a, c])
res = a | c

checkResults(n0, res)

n0.dump('graph.dot')


