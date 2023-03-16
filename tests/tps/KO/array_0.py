#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

m = Symb('m', 'M', 3)
k = Symb('k', 'S', 3)
a = ArrayExp('a', 3, 3, None, None, None, None)

e = m ^ a[k ^ m]

checkTpsResult(e, False)

