#!/usr/bin/python

from __future__ import print_function

from muse import *

order = 5
prop = 'ni'
withGlitches = False
dumpCirc = False
checkFunctionality = False

a = symbol('a', 'S', 1)
b = symbol('b', 'S', 1)

if prop == 'tps':
    a0, a1, a2, a3, a4, a5 = getPseudoShares(a, 6)
    b0, b1, b2, b3, b4, b5 = getPseudoShares(b, 6)
else:
    a0, a1, a2, a3, a4, a5 = getRealShares(a, 6)
    b0, b1, b2, b3, b4, b5 = getRealShares(b, 6)

a0 = inputGate(a0)
a1 = inputGate(a1)
a2 = inputGate(a2)
a3 = inputGate(a3)
a4 = inputGate(a4)
a5 = inputGate(a5)
b0 = inputGate(b0)
b1 = inputGate(b1)
b2 = inputGate(b2)
b3 = inputGate(b3)
b4 = inputGate(b4)
b5 = inputGate(b5)

r0 = symbol('r0', 'M', 1)
r1 = symbol('r1', 'M', 1)
r2 = symbol('r2', 'M', 1)
r3 = symbol('r3', 'M', 1)
r4 = symbol('r4', 'M', 1)
r5 = symbol('r5', 'M', 1)
r6 = symbol('r6', 'M', 1)
r7 = symbol('r7', 'M', 1)
r8 = symbol('r8', 'M', 1)
r9 = symbol('r9', 'M', 1)
r20 = symbol('r20', 'M', 1)
r21 = symbol('r21', 'M', 1)

r0 = inputGate(r0)
r1 = inputGate(r1)
r2 = inputGate(r2)
r3 = inputGate(r3)
r4 = inputGate(r4)
r5 = inputGate(r5)
r6 = inputGate(r6)
r7 = inputGate(r7)
r8 = inputGate(r8)
r9 = inputGate(r9)
r20 = inputGate(r20)
r21 = inputGate(r21)

a0b0 = andGate(a0, b0)
a0b1 = andGate(a0, b1)
a0b2 = andGate(a0, b2)
a0b3 = andGate(a0, b3)
a0b4 = andGate(a0, b4)
a0b5 = andGate(a0, b5)
a1b0 = andGate(a1, b0)
a1b1 = andGate(a1, b1)
a1b2 = andGate(a1, b2)
a1b3 = andGate(a1, b3)
a1b4 = andGate(a1, b4)
a1b5 = andGate(a1, b5)
a2b0 = andGate(a2, b0)
a2b1 = andGate(a2, b1)
a2b2 = andGate(a2, b2)
a2b3 = andGate(a2, b3)
a2b4 = andGate(a2, b4)
a2b5 = andGate(a2, b5)
a3b0 = andGate(a3, b0)
a3b1 = andGate(a3, b1)
a3b2 = andGate(a3, b2)
a3b3 = andGate(a3, b3)
a3b4 = andGate(a3, b4)
a3b5 = andGate(a3, b5)
a4b0 = andGate(a4, b0)
a4b1 = andGate(a4, b1)
a4b2 = andGate(a4, b2)
a4b3 = andGate(a4, b3)
a4b4 = andGate(a4, b4)
a4b5 = andGate(a4, b5)
a5b0 = andGate(a5, b0)
a5b1 = andGate(a5, b1)
a5b2 = andGate(a5, b2)
a5b3 = andGate(a5, b3)
a5b4 = andGate(a5, b4)
a5b5 = andGate(a5, b5)

alpha_0_0 = a0b0
alpha_0_1 = xorGate(a0b1, a1b0)
alpha_0_2 = xorGate(a0b2, a2b0)
alpha_0_3 = xorGate(a0b3, a3b0)
alpha_0_4 = xorGate(a0b4, a4b0)
alpha_0_5 = xorGate(a0b5, a5b0)
alpha_1_1 = a1b1
alpha_1_2 = xorGate(a1b2, a2b1)
alpha_1_3 = xorGate(a1b3, a3b1)
alpha_1_4 = xorGate(a1b4, a4b1)
alpha_1_5 = xorGate(a1b5, a5b1)
alpha_2_2 = a2b2
alpha_2_3 = xorGate(a2b3, a3b2)
alpha_2_4 = xorGate(a2b4, a4b2)
alpha_2_5 = xorGate(a2b5, a5b2)
alpha_3_3 = a3b3
alpha_3_4 = xorGate(a3b4, a4b3)
alpha_3_5 = xorGate(a3b5, a5b3)
alpha_4_4 = a4b4
alpha_4_5 = xorGate(a4b5, a5b4)
alpha_5_5 = a5b5

c0 = alpha_0_0
c1 = alpha_1_1
c2 = alpha_2_2
c3 = alpha_3_3
c4 = alpha_4_4
c5 = alpha_5_5

c0 = xorGate(c0, r0)
c0 = xorGate(c0, alpha_0_1)
c1 = xorGate(c1, r1)
c1 = xorGate(c1, alpha_1_2)
c2 = xorGate(c2, r2)
c2 = xorGate(c2, alpha_2_3)
c3 = xorGate(c3, r3)
c3 = xorGate(c3, alpha_3_4)
c4 = xorGate(c4, r4)
c4 = xorGate(c4, alpha_4_5)
c5 = xorGate(c5, r5)
c5 = xorGate(c5, alpha_0_5)
c0 = xorGate(c0, r1)
c0 = xorGate(c0, alpha_0_2)
c1 = xorGate(c1, r2)
c1 = xorGate(c1, alpha_1_3)
c2 = xorGate(c2, r3)
c2 = xorGate(c2, alpha_2_4)
c3 = xorGate(c3, r4)
c3 = xorGate(c3, alpha_3_5)
c4 = xorGate(c4, r5)
c4 = xorGate(c4, alpha_0_4)
c5 = xorGate(c5, r0)
c5 = xorGate(c5, alpha_1_5)
c0 = xorGate(c0, r6)
c0 = xorGate(c0, alpha_0_3)
c1 = xorGate(c1, r7)
c1 = xorGate(c1, alpha_1_4)
c2 = xorGate(c2, r8)
c2 = xorGate(c2, alpha_2_5)
c3 = xorGate(c3, r9)

c0 = xorGate(c0, r7)
c0 = xorGate(c0, r20)
c1 = xorGate(c1, r8)
c1 = xorGate(c1, r21)
c2 = xorGate(c2, r9)
c3 = xorGate(c3, r6)
c4 = xorGate(c4, r20)
c5 = xorGate(c5, r21)

if checkFunctionality:
    res, v0, v1 = compareExpsWithRandev(c0.symbExp ^ c1.symbExp ^ c2.symbExp ^ c3.symbExp ^ c4.symbExp ^ c5.symbExp, a & b, 100000)
    if res == None:
        print('# functionality (random evaluation): [OK]')
    else:
        print('# functionality (random evaluation): [KO]')
        print(res)

if dumpCirc:
    dumpCircuit('circuit.dot', c0, c1, c2, c3, c4, c5)

checkSecurity(order, withGlitches, prop, c0, c1, c2, c3, c4, c5)







