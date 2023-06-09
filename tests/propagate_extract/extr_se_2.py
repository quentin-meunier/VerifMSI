#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)
n = Extract(12, 4, SignExt(10, a))

a7 = Extract(7, 7, a)
wres = Concat(a7, a7, a7, a7, a7, Extract(7, 4, a))

checkResults(n, wres, pei = True)

n.dump('graph.dot')


