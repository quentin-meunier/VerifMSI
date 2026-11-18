#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

order = 3
secProp = 'NI'.lower()
withGlitches = False
dumpCirc = False
checkFunctionality = False
circuitFilename = "circuit.dot"
def isw_and_4_shares():
    a = symbol("a", 'S', 1)
    b = symbol("b", 'S', 1)
    u = getRealShares(a, 4)
    v = getRealShares(b, 4)
    _a0 = u[0]
    _a1 = u[1]
    _a2 = u[2]
    _a3 = u[3]
    _b0 = v[0]
    _b1 = v[1]
    _b2 = v[2]
    _b3 = v[3]
    a0 = inputGate(_a0)
    a1 = inputGate(_a1)
    a2 = inputGate(_a2)
    a3 = inputGate(_a3)
    b0 = inputGate(_b0)
    b1 = inputGate(_b1)
    b2 = inputGate(_b2)
    b3 = inputGate(_b3)
    _z0_1 = symbol("z0_1", 'M', 1)
    z0_1 = inputGate(_z0_1)
    a0b1 = andGate(a0, b1)
    a1b0 = andGate(a1, b0)
    z1_0 = xorGate(xorGate(z0_1, a0b1), a1b0)
    _z0_2 = symbol("z0_2", 'M', 1)
    z0_2 = inputGate(_z0_2)
    a0b2 = andGate(a0, b2)
    a2b0 = andGate(a2, b0)
    z2_0 = xorGate(xorGate(z0_2, a0b2), a2b0)
    _z0_3 = symbol("z0_3", 'M', 1)
    z0_3 = inputGate(_z0_3)
    a0b3 = andGate(a0, b3)
    a3b0 = andGate(a3, b0)
    z3_0 = xorGate(xorGate(z0_3, a0b3), a3b0)
    _z1_2 = symbol("z1_2", 'M', 1)
    z1_2 = inputGate(_z1_2)
    a1b2 = andGate(a1, b2)
    a2b1 = andGate(a2, b1)
    z2_1 = xorGate(xorGate(z1_2, a1b2), a2b1)
    _z1_3 = symbol("z1_3", 'M', 1)
    z1_3 = inputGate(_z1_3)
    a1b3 = andGate(a1, b3)
    a3b1 = andGate(a3, b1)
    z3_1 = xorGate(xorGate(z1_3, a1b3), a3b1)
    _z2_3 = symbol("z2_3", 'M', 1)
    z2_3 = inputGate(_z2_3)
    a2b3 = andGate(a2, b3)
    a3b2 = andGate(a3, b2)
    z3_2 = xorGate(xorGate(z2_3, a2b3), a3b2)
    c0a = andGate(a0, b0)
    c0b = xorGate(c0a, z0_1)
    c0c = xorGate(c0b, z0_2)
    c0 = xorGate(c0c, z0_3)
    c1a = andGate(a1, b1)
    c1b = xorGate(c1a, z1_0)
    c1c = xorGate(c1b, z1_2)
    c1 = xorGate(c1c, z1_3)
    c2a = andGate(a2, b2)
    c2b = xorGate(c2a, z2_0)
    c2c = xorGate(c2b, z2_1)
    c2 = xorGate(c2c, z2_3)
    c3a = andGate(a3, b3)
    c3b = xorGate(c3a, z3_0)
    c3c = xorGate(c3b, z3_1)
    c3 = xorGate(c3c, z3_2)
    if checkFunctionality:
        values = {}
        res = compareExpsWithExev(c0.getSymbExp() ^ c1.getSymbExp() ^ c2.getSymbExp() ^ c3.getSymbExp(), a & b, values)
        if res:
            print("# functionality (exhaustive evaluation): [OK]")
        else:
            print("# functionality (exhaustive evaluation): [KO]")
            for k, v in values.items():
                print("# value of ", k, ": ", v)
    if dumpCirc:
        outputs = [c0, c1, c2, c3]
        dumpCircuit("circuit.dot", outputs)
    outputs = [c0, c1, c2, c3]
    nbLeak = checkSecurity(order, withGlitches, secProp, outputs)
    return nbLeak
nbLeak = isw_and_4_shares()
print("# Total Nb. of potential leakages found: ", nbLeak)
assert(nbLeak == 0)
verifMSICleanup()
nbLeak = isw_and_4_shares()
print("# Total Nb. of potential leakages found: ", nbLeak)
assert(nbLeak == 0)
verifMSICleanup()
