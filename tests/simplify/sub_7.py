#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


p = symbol('p', 'P', 2)
q = symbol('q', 'P', 2)

n = -p + q

wres = q - p

checkResults(n, wres)


n.dump('graph.dot')


