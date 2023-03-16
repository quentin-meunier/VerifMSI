#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)
k1 = symbol('k1', 'S', 8)


exp_0 = ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 0), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) & SignExt(Const(31, 5), Extract(Const(0, 0), Const(0, 0), ((((ZeroExt(Const(24, 5), (m1 ^ k1)) >> Const(1, 1)) >> Const(1, 1)) >> Const(1, 1)) >> Const(1, 1))))
        
exp2_0 = ZeroExt(Const(24, 5), ((Concat(Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0)) & Const(27, 8)) ^ Concat(((Concat(Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0)) & Const(27, 7)) ^ Concat(((Concat(Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0)) & Const(27, 6)) ^ Concat(((Concat(Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 5)) ^ Concat(Extract(Const(3, 2), Const(0, 0), m0), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1)))) & SignExt(Const(31, 5), (Extract(Const(4, 3), Const(4, 3), m1) ^ Extract(Const(4, 3), Const(4, 3), k1)))


r, v0, v1 = compareExpsWithRandev(exp_0, exp2_0, 100)

if r == None:
    print('OK')
else:
    print('KO')



