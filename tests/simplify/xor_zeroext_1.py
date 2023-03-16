#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


k = symbol('k', 'S', 8)

n = ZeroExt(24, k) ^ ZeroExt(24, k) ^ ZeroExt(24, constant(12, 8))

wres = constant(12, 32)

checkResults(n, wres)



