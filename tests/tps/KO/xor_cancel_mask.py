#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


s = symbol('s', 'S', 1)
r = symbol('r', 'M', 1)

n = s ^ r ^ r

checkTpsResult(n, False)


