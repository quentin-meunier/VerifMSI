# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the Muse project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from verif_msi import *

order = 3
prop = 'ni'
withGlitches = False
dumpCirc = False
checkFunctionality = False

x = symbol('x', 'S', 1)
y = symbol('y', 'S', 1)

if prop == 'tps':
    x0, x1, x2, x3 = getPseudoShares(x, 4)
    y0, y1, y2, y3 = getPseudoShares(y, 4)
else:
    x0, x1, x2, x3 = getRealShares(x, 4)
    y0, y1, y2, y3 = getRealShares(y, 4)


x0 = inputGate(x0)
x1 = inputGate(x1)
x2 = inputGate(x2)
x3 = inputGate(x3)
y0 = inputGate(y0)
y1 = inputGate(y1)
y2 = inputGate(y2)
y3 = inputGate(y3)



x2_x3 = xorGate(x2, x3)
y1_y2 = xorGate(y1, y2)
t0 = andGate(x2_x3, y1_y2)
t1 = xorGate(t0, y1)
t2 = xorGate(t1, y2)
t3 = xorGate(t2, y3)
t4 = xorGate(t3, x1)
t5 = xorGate(t4, x2)
z0 = xorGate(t5, x3)

x0_x2 = xorGate(x0, x2)
y0_y3 = xorGate(y0, y3)
t0 = andGate(x0_x2, y0_y3)
t1 = xorGate(t0, y0)
t2 = xorGate(t1, y2)
t3 = xorGate(t2, y3)
t4 = xorGate(t3, x0)
t5 = xorGate(t4, x2)
z1 = xorGate(t5, x3)

x1_x3 = xorGate(x1, x3)
t0 = andGate(x1_x3, y0_y3)
t1 = xorGate(t0, y1)
z2 = xorGate(t1, x1)

x0_x1 = xorGate(x0, x1)
t0 = andGate(x0_x1, y1_y2)
t1 = xorGate(t0, y0)
z3 = xorGate(t1, x0)

 
if checkFunctionality:
    res, v0, v1 = compareExpsWithExev(z0.symbExp ^ z1.symbExp ^ z2.symbExp ^ z3.symbExp, x & y)
    if res == None:
        print('# functionality (exhaustive evaluation): [OK]')
    else:
        print('# functionality (exhaustive evaluation): [KO]')
        print(res)

if dumpCirc:
    dumpCircuit('circuit.dot', z0, z1, z2, z3)

checkSecurity(order, withGlitches, prop, z0, z1, z2, z3)



