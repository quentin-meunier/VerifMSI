#!/usr/bin/python

from __future__ import print_function

from verif_msi import *



k = symbol('k', 'S', 8)
p = symbol('p', 'P', 8)

m0 = symbol('m0', 'M', 8)
p1 = symbol('p1', 'P', 8)
p2 = symbol('p2', 'P', 8)

n0 = k ^ m0

n1 = p1 + n0
n2 = n0 + p2
n3 = ~n2
n4 = n1 & n3
n5 = ~n4
n6 = m0 ^ k
n7 = n6 + p
n8 = n5 + n4 + n6 + n7

#n8.dump('graph.dot')

checkTpsResult(n8, True)


