#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

m = symbol('m', 'M', 3)
k = symbol('k', 'S', 3)
p = symbol('p', 'P', 3)
a = ArrayExp('a', 3, 3, None, None, None, None)

e = m ^ a[((k ^ m) << 1) ^ (m << 1) ^ p]

checkTpsResult(e, True)

