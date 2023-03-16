#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

a = symbol('a', 'P', 8)
u = Extract(0, 0, Extract(0, 0, Extract(0, 0, Extract(0, 0, ~a))))
v = Extract(0, 0, Extract(0, 0, Extract(0, 0, ~a)))
n = u ^ v

wres = constant(0, 1)


checkResults(n, wres, pei = True)



