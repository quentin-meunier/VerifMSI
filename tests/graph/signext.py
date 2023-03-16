#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


s = symbol('s', 'S', 4)
m = symbol('m', 'M', 4)

n = SignExt(8, s ^ m)

n.dump('graph.dot')



