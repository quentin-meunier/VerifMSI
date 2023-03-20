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
        global nbExps
        global nbLeak
        self.val = val

        if self.oldVal == None:
            self.oldVal = constant(0, self.val.width)
        
        nbExps += 1
        res, wordRes, niTime = checkTpsTrans(self.oldVal, self.val)
        if not res:
            nbLeak += 1
            print('# Leakage in transition for check %d (Total leaks : %d)' % (nbExps, nbLeak))
        self.oldVal = self.val



def compute(x, y, r, u, v):
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
    tmp.setVal(RotateRight(a.val, 32))
    tmp.setVal(tmp.val & b.val)
    c.setVal(c.val ^ tmp.val)
    tmp.setVal(RotateRight(b.val, 48))
    tmpr.setVal(u)
    c.setVal(c.val ^ tmpr.val)
    tmp.setVal(tmp.val & a.val)
    c.setVal(c.val ^ tmp.val)
    tmp.setVal(RotateRight(a.val, 48))
    tmp.setVal(tmp.val & b.val)
    c.setVal(c.val ^ tmp.val)
    tmpr.setVal(RotateRight(tmpr.val, 16))
    c.setVal(c.val ^ tmpr.val)
    tmp.setVal(RotateRight(b.val, 64))
    tmp.setVal(tmp.val & a.val)
    c.setVal(c.val ^ tmp.val)
    tmpr.setVal(v)
    c.setVal(c.val ^ tmpr.val)
    tmpr.setVal(RotateRight(tmpr.val, 16))
    c.setVal(c.val ^ tmpr.val)
    v = c.val
    return Extract(15, 0, v), Extract(31, 16, v), Extract(47, 32, v), Extract(63, 48, v), Extract(79, 64, v), Extract(95, 80, v), Extract(111, 96, v), Extract(127, 112, v)




def vector_mult_8_shares():

    testLitteral = False

    if not testLitteral:
        x = symbol('x', 'S', 16)
        y = symbol('y', 'S', 16)
        x0, x1, x2, x3, x4, x5, x6, x7 = getPseudoShares(x, 8)
        y0, y1, y2, y3, y4, y5, y6, y7 = getPseudoShares(y, 8)

        r0 = symbol('r0', 'M', 16)
        r1 = symbol('r1', 'M', 16)
        r2 = symbol('r2', 'M', 16)
        r3 = symbol('r3', 'M', 16)
        r4 = symbol('r4', 'M', 16)
        r5 = symbol('r5', 'M', 16)
        r6 = symbol('r6', 'M', 16)
        r7 = symbol('r7', 'M', 16)

        r8 = symbol('r8', 'M', 16)
        r9 = symbol('r9', 'M', 16)
        r10 = symbol('r10', 'M', 16)
        r11 = symbol('r11', 'M', 16)
        r12 = symbol('r12', 'M', 16)
        r13 = symbol('r13', 'M', 16)
        r14 = symbol('r14', 'M', 16)
        r15 = symbol('r15', 'M', 16)

        r16 = symbol('r16', 'M', 16)
        r17 = symbol('r17', 'M', 16)
        r18 = symbol('r18', 'M', 16)
        r19 = symbol('r19', 'M', 16)
        r20 = symbol('r20', 'M', 16)
        r21 = symbol('r21', 'M', 16)
        r22 = symbol('r22', 'M', 16)
        r23 = symbol('r23', 'M', 16)

    else:
        x0 = constant(0xb945, 16)
        x1 = constant(0x45af, 16)
        x2 = constant(0xdefd, 16)
        x3 = constant(0xa654, 16)
        x4 = constant(0xb123, 16)
        x5 = constant(0x639d, 16)
        x6 = constant(0xc386, 16)
        x7 = constant(0xae76, 16)

        y0 = constant(0xab81, 16)
        y1 = constant(0x3d0e, 16)
        y2 = constant(0x7f83, 16)
        y3 = constant(0xfe48, 16)
        y4 = constant(0x83c8, 16)
        y5 = constant(0x22b3, 16)
        y6 = constant(0x904c, 16)
        y7 = constant(0x1b40, 16)

        r0 = constant(0x6ebd, 16)
        r1 = constant(0xf2d1, 16)
        r2 = constant(0xae26, 16)
        r3 = constant(0x33ef, 16)
        r4 = constant(0x9877, 16)
        r5 = constant(0xabcd, 16)
        r6 = constant(0x813a, 16)
        r7 = constant(0xf4e6, 16)

        r8 = constant(0x70df, 16)
        r9 = constant(0x227d, 16)
        r10 = constant(0x4510, 16)
        r11 = constant(0xde8f, 16)
        r12 = constant(0x71a3, 16)
        r13 = constant(0x823e, 16)
        r14 = constant(0xe8b1, 16)
        r15 = constant(0x09aa, 16)

        r16 = constant(0x7131, 16)
        r17 = constant(0xb1a1, 16)
        r18 = constant(0xa7f4, 16)
        r19 = constant(0xff41, 16)
        r20 = constant(0xf98c, 16)
        r21 = constant(0xa7a5, 16)
        r22 = constant(0x7420, 16)
        r23 = constant(0xbabe, 16)

    x = Concat(x0, x1, x2, x3, x4, x5, x6, x7)
    y = Concat(y0, y1, y2, y3, y4, y5, y6, y7)
    r = Concat(r0, r1, r2, r3, r4, r5, r6, r7)
    u = Concat(r8, r9, r10, r11, r12, r13, r14, r15)
    v = Concat(r16, r17, r18, r19, r20, r21, r22, r23)

    # start analysis
    z0, z1, z2, z3, z4, z5, z6, z7 = compute(x, y, r, u, v)
    # end analysis

    if testLitteral:
        x = x0 ^ x1 ^ x2 ^ x3 ^ x4 ^ x5 ^ x6 ^ x7
        y = y0 ^ y1 ^ y2 ^ y3 ^ y4 ^ y5 ^ y6 ^ y7
        z = z0 ^ z1 ^ z2 ^ z3 ^ z4 ^ z5 ^ z6 ^ z7
        res = x & y
        print('# x = %s' % x)
        print('# y = %s' % y)
        print('# x & y = %s' % res)
        print('# z     = %s' % z)

    global nbLeak, nbExps
    return nbLeak, nbExps



if __name__ == '__main__':
    nbLeak, nbExps = vector_mult_8_shares()
    print('# Total Nb. of expressions analysed: %d' % nbExps)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)




