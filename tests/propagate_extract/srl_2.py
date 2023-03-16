#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 32)

n = Extract(26, 5, LShR(a, 10))

wres = Concat(constant(0, 5), Extract(31, 15, a))

checkResults(n, wres, pei = True)

a.dump('graph.dot')


