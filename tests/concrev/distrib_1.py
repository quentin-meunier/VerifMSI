#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random

m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)
k1 = symbol("k1", 'S', 8)

exp_0 = Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1)))) & SignExt(Const(7, 5), Extract(Const(0, 1), Const(0, 1), ((((ZeroExt(Const(24, 5), (m1 ^ k1)) >> Const(1, 1)) >> Const(1, 1)) >> Const(1, 1)) >> Const(1, 1))))

exp_1 = Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1)))))) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), Extract(Const(7, 3), Const(0, 1), ((SignExt(Const(31, 5), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 32)) ^ (ZeroExt(Const(24, 5), m0) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))) << Const(1, 1))))


rud

# Node & es = simplify(exp_0, true, true);
# std::cout << "es : " << es << std::endl;

sid = getDistribWithExev(exp_0, rud)

if not rud and sid:
    print("OK")
else:
    print("KO")


sid = getDistribWithExev(exp_1, rud)

if rud and sid:
    print("OK")
else:
    print("KO")


sid = getDistribWithExev(exp_0 ^ exp_1, rud)

if rud and sid:
    print("OK")
else:
    print("KO")


