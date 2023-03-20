# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the Muse project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from verif_msi import *


order = 1
prop = 'ni'
withGlitches = False
dumpCirc = False
checkFunctionality = False

a = symbol('a', 'S', 1)
b = symbol('b', 'S', 1)
z = symbol('z', 'M', 1)

if prop == 'tps':
    a0, a1 = getPseudoShares(a, 2)
    b0, b1 = getPseudoShares(b, 2)
else:
    a0, a1 = getRealShares(a, 2)
    b0, b1 = getRealShares(b, 2)


a0 = inputGate(a0)
a1 = inputGate(a1)
b0 = inputGate(b0)
b1 = inputGate(b1)
z = inputGate(z)



# output s = s0 ^ s1 = a & b

# s0 = (a1 & b1 ^ a0 & b1 ^ b0 & a1 ^ a0 & b0) ^ z
# s1 = z

c0 = andGate(a0, b0)
c1 = andGate(b0, a1)
c2 = andGate(a0, b1)
c3 = andGate(a1, b1)

c4 = xorGate(z, c0)
c5 = xorGate(c1, c4)
c6 = xorGate(c2, c5)
s0 = xorGate(c6, c3)

s1 = z


if checkFunctionality:
    res, v0, v1 = compareExpsWithExev(s0.symbExp ^ s1.symbExp, a & b)
    if res == None:
        print('# functionality (exhaustive evaluation): [OK]')
    else:
        print('# functionality (exhaustive evaluation): [KO]')
        print(res)

if dumpCirc:
    dumpCircuit('circuit.dot', s0, s1)

checkSecurity(order, withGlitches, prop, s0, s1)




