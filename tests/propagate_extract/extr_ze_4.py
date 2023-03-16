#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 8)
n = Extract(8, 0, ZeroExt(10, a))

wres = Concat(constant(0, 1), a)

checkResults(n, wres, pei = True)

n.dump('graph.dot')


