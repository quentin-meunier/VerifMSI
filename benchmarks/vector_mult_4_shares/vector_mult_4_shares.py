# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the Muse project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function

from verif_msi import *


nbLeak = 0
nbExps = 0


class Register:
    def __init__(self):
        self.oldVal = None
        self.newVal = None

    def setVal(self, val):
        global nbLeak
        global nbExps
        self.val = val

        if self.oldVal == None:
            self.oldVal = constant(0, self.val.width)
        
        nbExps += 1
        res, wordRes, niTime = checkTpsTrans(self.oldVal, self.val)
        if not res:
            nbLeak += 1
            print('# Leakage in transition for check %d (Total leaks : %d)' % (nbExps, nbLeak))
        self.oldVal = self.val



def compute(x, y, r, r4):
    a = Register()
    b = Register()
    c = Register()
    tmp = Register()
    tmpr = Register()
    a.setVal(x)
    b.setVal(y)
    c.setVal(a.val & b.val)
    tmpr.setVal(r)
    tmp.setVal(RotateRight(b.val, 16))
    c.setVal(c.val ^ tmpr.val)
    tmp.setVal(tmp.val & a.val)
    c.setVal(c.val ^ tmp.val)
    tmp.setVal(RotateRight(a.val, 16))
    tmp.setVal(tmp.val & b.val)
    c.setVal(c.val ^ tmp.val)
    tmpr.setVal(RotateRight(tmpr.val, 16))
    c.setVal(c.val ^ tmpr.val)
    tmp.setVal(RotateRight(b.val, 32))
    tmp.setVal(tmp.val & a.val)
    c.setVal(c.val ^ tmp.val)
    tmp.setVal(Concat(r4, r4, r4, r4))
    c.setVal(c.val ^ tmp.val)
    return Extract(15, 0, c.val), Extract(31, 16, c.val), Extract(47, 32, c.val), Extract(63, 48, c.val)




def vector_mult_4_shares():

    testLitteral = False

    if not testLitteral:
        x = symbol('x', 'S', 16)
        y = symbol('y', 'S', 16)
        x0, x1, x2, x3 = getPseudoShares(x, 4)
        y0, y1, y2, y3 = getPseudoShares(y, 4)

        r0 = symbol('r0', 'M', 16)
        r1 = symbol('r1', 'M', 16)
        r2 = symbol('r2', 'M', 16)
        r3 = symbol('r3', 'M', 16)

        r4 = symbol('r4', 'M', 16)

    else:
        x0 = constant(0xb945, 16)
        x1 = constant(0x45af, 16)
        x2 = constant(0xdefd, 16)
        x3 = constant(0xa654, 16)

        y0 = constant(0xab81, 16)
        y1 = constant(0x3d0e, 16)
        y2 = constant(0x7f83, 16)
        y3 = constant(0xfe48, 16)

        r0 = constant(0x6ebd, 16)
        r1 = constant(0xf2d1, 16)
        r2 = constant(0xae26, 16)
        r3 = constant(0x33ef, 16)
        r4 = constant(0x9877, 16)

    x = Concat(x0, x1, x2, x3)
    y = Concat(y0, y1, y2, y3)
    r = Concat(r0, r1, r2, r3)

    # start analysis
    z0, z1, z2, z3 = compute(x, y, r, r4)
    # end analysis

    if testLitteral:
        x = x0 ^ x1 ^ x2 ^ x3
        y = y0 ^ y1 ^ y2 ^ y3
        z = z0 ^ z1 ^ z2 ^ z3
        res = x & y
        print('# x = %s' % x)
        print('# y = %s' % y)
        print('# x & y = %s' % res)
        print('# z  = %s' % z)

    global nbLeak, nbExps
    return nbLeak, nbExps


if __name__ == '__main__':
    nbLeak, nbExps = vector_mult_4_shares()
    print('# Total Nb. of expressions analysed: %d' % nbExps)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)




