# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the Muse project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from verif_msi import *


order = 2
prop = 'ni'
withGlitches = False
dumpCirc = False
checkFunctionality = False


a = symbol('a', 'S', 1)
b = symbol('b', 'S', 1)

if prop == 'tps':
    a0, a1, a2 = getPseudoShares(a, 3)
    b0, b1, b2 = getPseudoShares(b, 3)
else:
    a0, a1, a2 = getRealShares(a, 3)
    b0, b1, b2 = getRealShares(b, 3)

z12 = symbol('z12', 'M', 1)
z13 = symbol('z13', 'M', 1)
z23 = symbol('z23', 'M', 1)

a0 = inputGate(a0)
a1 = inputGate(a1)
a2 = inputGate(a2)
b0 = inputGate(b0)
b1 = inputGate(b1)
b2 = inputGate(b2)

z12 = inputGate(z12)
z13 = inputGate(z13)
z23 = inputGate(z23)


# Non linear layer
a0b0 = andGate(a0, b0)
a0b1 = andGate(a0, b1)
a0b2 = andGate(a0, b2)
a1b0 = andGate(a1, b0)
a1b1 = andGate(a1, b1)
a1b2 = andGate(a1, b2)
a2b0 = andGate(a2, b0)
a2b1 = andGate(a2, b1)
a2b2 = andGate(a2, b2)

# Linear Layer
l00 = xorGate(a0b0, a2b0)
l0 = xorGate(l00, a0b2)
l10 = xorGate(a1b0, a0b1)
l1 = xorGate(l10, a1b1)
l20 = xorGate(a2b1, a1b2)
l2 = xorGate(l20, a2b2)

# Refreshing Layer
c00 = xorGate(l0, z12)
c0 = xorGate(c00, z13)
c10 = xorGate(l1, z12)
c1 = xorGate(c10, z23)
c20 = xorGate(l2, z13)
c2 = xorGate(c20, z23)
 
 
if checkFunctionality:
    res, v0, v1 = compareExpsWithExev(c0.symbExp ^ c1.symbExp ^ c2.symbExp, a & b)
    if res == None:
        print('# functionality (exhaustive evaluation): [OK]')
    else:
        print('# functionality (exhaustive evaluation): [KO]')
        print(res)

if dumpCirc:
    dumpCircuit('circuit.dot', c0, c1, c2)

checkSecurity(order, withGlitches, prop, c0, c1, c2)



