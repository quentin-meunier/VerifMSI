
from verif_msi import *

 

x = symbol('x', 'S', 1)
y = symbol('y', 'S', 1)
r = symbol('r', 'M', 1)

src0 = x & y | x + y
trg0 = x ^ y

src1 = x & y ^ x + y ^ r
trg1 = x & y ^ r

addSimpRule(src0, trg0)
addSimpRule(src1, trg1)

a = symbol('a', 'P', 4)
b = symbol('b', 'P', 4)
m = symbol('m', 'M', 4)

e = a & b ^ a + b ^ m

print('e : %s' % e)
f = getEquiv(e)
print('f : %s' % f)




