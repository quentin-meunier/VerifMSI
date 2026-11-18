#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)
k2 = symbol("k2", 'S', 8)

m0 = symbol("m0", 'M', 8)
m1 = symbol("m1", 'M', 8)
m2 = symbol("m2", 'M', 8)

p0 = symbol("p0", 'P', 8)
p1 = symbol("p1", 'P', 8)
p2 = symbol("p2", 'P', 8)


n0 = (m0 & k0)
checkTpsResult(n0, False)

n1 = (~m0 & k0)
checkTpsResult(n1, False)

n2 = (~~m0 & k0)
checkTpsResult(n2, False)

n3 = (~~~m0 & k0)
checkTpsResult(n3, False)

n4 = (k0 & (p0 ^ m0))
checkTpsResult(n4, False)

n5 = (k0 & (p0 ^ ~m0))
checkTpsResult(n5, False)

n6 = (k0 & (p0 ^ ~~m0))
checkTpsResult(n6, False)



n7 = (m0 ^ k0)
checkTpsResult(n7, True)

n8 = (~m0 ^ k0)
checkTpsResult(n8, True)

n9 = (~~m0 ^ k0)
checkTpsResult(n9, True)

n10 = (~~~m0 ^ k0)
checkTpsResult(n10, True)

n11 = (k0 ^ (p0 ^ m0))
checkTpsResult(n11, True)

n12 = (k0 ^ (p0 ^ ~m0))
checkTpsResult(n12, True)

n13 = (k0 ^ (p0 ^ ~~m0))
checkTpsResult(n13, True)



n14 = (m1 ^ k1) & (m0 ^ k0)
checkTpsResult(n14, True)

n15 = (m1 ^ k1) & (~m0 ^ k0)
checkTpsResult(n15, True)

n16 = (m1 ^ k1) & (~~m0 ^ k0)
checkTpsResult(n16, True)

n17 = (m1 ^ k1) & (~~~m0 ^ k0)
checkTpsResult(n17, True)

n18 = (m1 ^ k1) & (k0 ^ (p0 ^ m0))
checkTpsResult(n18, True)

n19 = (m1 ^ k1) & (k0 ^ (p0 ^ ~m0))
checkTpsResult(n19, True)

n20 = (m1 ^ k1) & (k0 ^ (p0 ^ ~~m0))
checkTpsResult(n20, True)



n21 = ((m0 ^ k0) & p0) & k2
checkTpsResult(n21, False)

n22 = (~((m0 ^ k0) + (k1 & m1)) & p1) ^ (m1 ^ k2)
checkTpsResult(n22, True)

n23 = (~((m0 ^ k0) + (k1 & m0)) & p1) ^ (m0 ^ k2)
checkTpsResult(n23, False)

n24 = (~((m0 ^ k0) + (k1 ^ m1)) & p1) ^ (m0 ^ k0)
checkTpsResult(n24, True)


