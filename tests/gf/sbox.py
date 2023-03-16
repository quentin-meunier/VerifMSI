#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

a = symbol('a', 'S', 8)
#b = symbol('b', 'S', 8)

a1 = symbol('a1', 'M', 8)
#b1 = symbol('b1', 'M', 8)

a0 = a ^ a1
#b0 = b ^ b1

randCnt = 0
def getNewRandom():
    global randCnt
    r = symbol('r_%d' % randCnt, 'M', 8)
    randCnt += 1
    return r


def mult(a0, a1, b0, b1):
    r01 = getNewRandom()
    r10 = r01 ^ (GExp(a0 + b1))
    r10 ^= GExp(a1 + b0)
    c0 = r10 ^ GExp(a1 + b1)
    c1 = r01 ^ GExp(a0 + b0)
    return c0, c1


def exp254(a0, a1):
    r0_2 = GPow(a0, constant(2, 8))
    r1_2 = GPow(a1, constant(2, 8))
    r0_3, r1_3 = mult(GLog(a0), GLog(a1), GLog(r0_2), GLog(r1_2))
    #print('r_3: %s' % simplify(r0_3 ^ r1_3))
    #sys.exit(0)

    r0_12 = GPow(r0_3, constant(4, 8))
    r1_12 = GPow(r1_3, constant(4, 8))

    r0_15, r1_15 = mult(GLog(r0_3), GLog(r1_3), GLog(r0_12), GLog(r1_12))

    r0_240 = GPow(r0_15, constant(16, 8))
    r1_240 = GPow(r1_15, constant(16, 8))

    r0_252, r1_252 = mult(GLog(r0_240), GLog(r1_240), GLog(r0_12), GLog(r1_12))
    r0_254, r1_254 = mult(GLog(r0_252), GLog(r1_252), GLog(r0_2), GLog(r1_2))

    return r0_254, r1_254

 

c0, c1 = exp254(a0, a1)

c = simplify(c0 ^ c1)

print('c = %s' % c)



