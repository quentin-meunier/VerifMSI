#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


# same as k9, but order of xor is different:
# matters because the xor is binary
# and k ^ k ^ 1 actually is:
#     ^
#    / \
#   ^   1
#  / \
# k   k

# &          &
#  \          \
#   \     ->   \
#    \          \
#     ^          \
#    /|\          \
#   k k 1          1


k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
c0 = constant(255, 8)

n0 = k0 ^ k0 ^ c0
n1 = n0 & k1

wres = k1

checkResults(n1, wres)

n1.dump('graph.dot')


