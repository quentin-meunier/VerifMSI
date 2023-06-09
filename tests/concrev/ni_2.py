#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)
k1 = symbol('k1', 'S', 8)



exp_0 = ((Concat(Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0)) & Const(27, 8)) ^ Concat(((Concat(Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0)) & Const(27, 7)) ^ Concat(((Concat(Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0)) & Const(27, 6)) ^ Concat(((Concat(Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 5)) ^ Concat(Extract(Const(3, 2), Const(0, 0), m0), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1))) & SignExt(Const(7, 5), (Extract(Const(4, 3), Const(4, 3), m1) ^ Extract(Const(4, 3), Const(4, 3), k1)))


exp_1 = (Concat((Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0))) & Const(27, 8)) ^ Concat(((Concat(Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0)) & Const(27, 7)) ^ Concat(((Concat(Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0)) & Const(27, 6)) ^ Concat(((Concat(Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0)) & Const(27, 5)) ^ Concat(((Concat(Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0)) & Const(11, 4)) ^ Concat(Extract(Const(2, 2), Const(0, 0), m0), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1))



res, useBE, time = checkTpsVal(exp_0 ^ exp_1)
print('TPS : %r' % res)





m0_0 = symbol('m0_0', 'M', 1)
m0_1 = symbol('m0_1', 'M', 1)
m0_2 = symbol('m0_2', 'M', 1)
m0_3 = symbol('m0_3', 'M', 1)
m0_4 = symbol('m0_4', 'M', 1)
m0_5 = symbol('m0_5', 'M', 1)
m0_6 = symbol('m0_6', 'M', 1)
m0_7 = symbol('m0_7', 'M', 1)

m1_4 = symbol('m1_4', 'M', 1)

k1_4 = symbol('k1_4', 'S', 1)


e = Concat(m0_2, m0_1, m0_0, m0_6, m0_5, (((((((((((((m0_7 ^ m0_3) & Concat((m1_4 ^ k1_4))) ^ m0_2) & Concat((m1_4 ^ k1_4))) ^ m0_1) & Concat((m1_4 ^ k1_4))) ^ m0_0) & Concat((m1_4 ^ k1_4))) ^ m0_3 ^ m0_6 ^ m0_7) & Concat((m1_4 ^ k1_4))) ^ m0_7 ^ m0_5 ^ m0_3) & Concat(m1_4)) ^ ((((((((((m0_7 ^ m0_3) & Concat((m1_4 ^ k1_4))) ^ m0_2) & Concat((m1_4 ^ k1_4))) ^ m0_1) & Concat((m1_4 ^ k1_4))) ^ m0_0) & Concat((m1_4 ^ k1_4))) ^ m0_3 ^ m0_6 ^ m0_7) & Concat((m1_4 ^ k1_4))) ^ m0_7 ^ m0_5 ^ ((((((((m0_7 ^ m0_3) & Concat((m1_4 ^ k1_4))) ^ m0_2) & Concat((m1_4 ^ k1_4))) ^ m0_1) & Concat((m1_4 ^ k1_4))) ^ m0_0) & Concat((m1_4 ^ k1_4))) ^ m0_6), m0_4, (((((((((((((((m0_7 ^ m0_3) & Concat(m1_4)) ^ m0_2) & Concat(m1_4)) ^ m0_1) & Concat(m1_4)) ^ m0_0) & Concat(m1_4)) ^ m0_3 ^ m0_6 ^ m0_7) & Concat(m1_4)) ^ m0_7 ^ m0_5 ^ ((((((((m0_7 ^ m0_3) & Concat(m1_4 ^ k1_4)) ^ m0_2) & Concat(m1_4 ^ k1_4)) ^ m0_1) & Concat(m1_4 ^ k1_4)) ^ m0_0) & Concat((m1_4 ^ k1_4))) ^ m0_6) & Concat(m1_4)) ^ m0_7 ^ m0_3 ^ m0_4) & m1_4) ^ m0_7 ^ m0_3))

rud, sid = getDistribWithExev(e)
print('LV exp 0 ^ exp 1')
print('RUD: %r' % rud)
print('SID: %r' % sid)


