#!/usr/bin/python

from __future__ import print_function

from verif_msi import *



k = symbol('k', 'S', 8)
n0 = SignExt(24, k)
n1 = Extract(7, 7, n0)

n2 = Extract(7, 7, k)
checkResults(n1, n2)

n1.dump('graph.dot')


