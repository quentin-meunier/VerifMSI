# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Etienne Pons, Quentin L. Meunier

from verif_msi import *


nbCheck = 0
nbLeak = 0

def checkExpLeakage(e):
    global nbCheck
    global nbLeak

    nbCheck += 1

    res, wordRes, niTime = checkTpsVal(e)
    if not res:
        nbLeak += 1
        print('# Leakage in value for exp num %d (Total leaks : %d)' % (nbCheck, nbLeak))


def secmult_sm():

    testLitteral = False

    if not testLitteral:
        m0 = symbol('m0', 'M', 8)
        m1 = symbol('m1', 'M', 8)
        r01 = symbol('m01', 'M', 8)

        k0 = symbol('k0', 'S', 8)
        k1 = symbol('k1', 'S', 8)
    else:
        m0 = constant(0xba, 8)
        m1 = constant(0x66, 8)
        r01 = constant(0x38, 8)

        k0 = constant(0xa1, 8)
        k1 = constant(0x0f, 8)

 
    a0 = m0
    b0 = m1
    a1 = m0 ^ k0
    b1 = m1 ^ k1

    p0_01 = GMul(a0, b1)
    p0_01 = simplify(p0_01)
    checkExpLeakage(p0_01)
    r10 = r01 ^ p0_01
    r10 = simplify(r10)
    checkExpLeakage(r10)
    p0_10 = GMul(a1, b0)
    p0_10 = simplify(p0_10)
    checkExpLeakage(p0_10)
    r10 = r10 ^ p0_10
    r10 = simplify(r10)
    checkExpLeakage(r10)
    c0 = GMul(a0, b0)
    c0 = simplify(c0)
    checkExpLeakage(c0)
    c0 = c0 ^ r01
    c0 = simplify(c0)
    checkExpLeakage(c0)
    c1 = GMul(a1, b1)
    c1 = simplify(c1)
    checkExpLeakage(c1)
    c1 = c1 ^ r10
    c1 = simplify(c1)
    checkExpLeakage(c1)

    if testLitteral:
        print('c0 = 0x%x' % int(str(c0), 0))
        print('c1 = 0x%x' % int(str(c1), 0))
        print('c0 ^ c1 = 0x%x' % (int(str(simplify(c0 ^ c1)), 0)))
        print('k0 * k1 = 0x%x' % (int(str(gmul(k0, k1)), 0)))
    

    global nbLeak, nbCheck
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = secmult_sm()
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)


