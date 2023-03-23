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
    a = symbol('a', 'S', 8)
    b = symbol('b', 'S', 8)
    
    a0 = symbol('a0', 'M', 8)
    b0 = symbol('b0', 'M', 8)
    
    r0_01 = symbol('r0_01', 'M', 8)
    
    a1 = a ^ a0
    a1 = simplify(a1)
    checkExpLeakage(a1)
    b1 = b ^ b0
    b1 = simplify(b1)
    checkExpLeakage(b1)
    p0_01 = GMul(a0, b1)
    p0_01 = simplify(p0_01)
    checkExpLeakage(p0_01)
    r0_10 = r0_01 ^ p0_01
    r0_10 = simplify(r0_10)
    checkExpLeakage(r0_10)
    p0_10 = GMul(a1, b0)
    p0_10 = simplify(p0_10)
    checkExpLeakage(p0_10)
    r0_10 = r0_10 ^ p0_10
    r0_10 = simplify(r0_10)
    checkExpLeakage(r0_10)
    c0 = GMul(a0, b0)
    c0 = simplify(c0)
    checkExpLeakage(c0)
    c0 = c0 ^ r0_01
    c0 = simplify(c0)
    checkExpLeakage(c0)
    c1 = GMul(a1, b1)
    c1 = simplify(c1)
    checkExpLeakage(c1)
    c1 = c1 ^ r0_10
    c1 = simplify(c1)
    checkExpLeakage(c1)

    global nbLeak, nbCheck
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = secmult_sm()
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)


