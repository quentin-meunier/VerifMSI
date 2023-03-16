#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

m = symbol('m', 'M', 8)
n0 = ~m
n1 = ~m

n0.printMaskOcc()
n1.printMaskOcc()

e = n0 + n1

e.printMaskOcc()
e.dump('graph.dot')



