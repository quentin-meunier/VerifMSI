#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

m = symbol('m', 'M', 8)
n = ~m

n.printMaskOcc()

e = n + n

e.printMaskOcc()




