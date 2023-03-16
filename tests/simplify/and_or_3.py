#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


a = symbol('a', 'P', 4)

e = a - a

print('%s' % getBitDecomposition(e))



