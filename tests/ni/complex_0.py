
from verif_msi import *


a = symbol('a', 'S', 1)
b = symbol('b', 'S', 1)

a2 = symbol('a2', 'M', 1)
a3 = symbol('a3', 'M', 1)

b2 = symbol('b2', 'M', 1)
b3 = symbol('b3', 'M', 1)

z0_4 = symbol('z0_4', 'M', 1)
z1_4 = symbol('z1_4', 'M', 1)
z2_4 = symbol('z2_4', 'M', 1)
z3_4 = symbol('z3_4', 'M', 1)


e = Concat(a2, z3_4,
    ((b ^ b3) & a3) ^ z1_4 ^ z2_4 ^ z3_4 ^ z0_4 ^ (a & b3),
    z1_4 ^ ((a2 ^ a) & b3) ^ z2_4 ^ z0_4 ^ ((b ^ b2 ^ b3) & a3))

res, dummy, time = checkTpsVal(e)

if res:
    print('# TPS')
else:
    print('# Not TPS')


e = ((b ^ b3) & a3) ^ (a & b3) ^ ((a2 ^ a) & b3) ^ (b2 & a3)

res, dummy, time = checkTpsVal(e)

if res:
    print('# TPS')
else:
    print('# Not TPS')





e = Concat(((b ^ b3) & a3) ^ z1_4 ^ z2_4 ^ z3_4 ^ z0_4 ^ (a & b3),
           (a2 & b3) ^ z3_4,
           z1_4 ^ ((a2 ^ a) & b3) ^ z2_4 ^ z0_4 ^ ((b ^ b2 ^ b3) & a3),
           z3_4)

res, dummy, time = checkTpsVal(e)

if res:
    print('# TPS')
else:
    print('# Not TPS')



