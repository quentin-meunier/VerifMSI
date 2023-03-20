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

x = symbol('x', 'S', 1)
y = symbol('y', 'S', 1)

if prop == 'tps':
    x0, x1, x2 = getPseudoShares(x, 3)
    y0, y1, y2 = getPseudoShares(y, 3)
else:
    x0, x1, x2 = getRealShares(x, 3)
    y0, y1, y2 = getRealShares(y, 3)


x0 = inputGate(x0)
x1 = inputGate(x1)
x2 = inputGate(x2)
y0 = inputGate(y0)
y1 = inputGate(y1)
y2 = inputGate(y2)


x0y0 = andGate(x0, y0)
x0y1 = andGate(x0, y1)
x0y2 = andGate(x0, y2)
x1y0 = andGate(x1, y0)
x1y1 = andGate(x1, y1)
x1y2 = andGate(x1, y2)
x2y0 = andGate(x2, y0)
x2y1 = andGate(x2, y1)
x2y2 = andGate(x2, y2)


t0 = xorGate(x1y1, x1y2)
z0 = xorGate(t0, x2y1)
t1 = xorGate(x2y2, x0y2)
z1 = xorGate(t1, x2y0)
t2 = xorGate(x0y0, x0y1)
z2 = xorGate(t2, x1y0)

 
if checkFunctionality:
    res, v0, v1 = compareExpsWithExev(z0.symbExp ^ z1.symbExp ^ z2.symbExp, x & y)
    if res == None:
        print('# functionality (exhaustive evaluation): [OK]')
    else:
        print('# functionality (exhaustive evaluation): [KO]')
        print(res)

if dumpCirc:
    dumpCircuit('circuit.dot', z0, z1, z2)

checkSecurity(order, withGlitches, prop, z0, z1, z2)



