
from verif_msi import *


x = symbol('x', 'S', 1)
y = symbol('y', 'S', 1)
r = symbol('r', 'M', 1)

src = x & x & y & y & x 
print('src: %s' % src)
trg = x ^ y

addSimpRule(src, trg)

a = symbol('a', 'P', 4)
b = symbol('b', 'P', 4)
m = symbol('m', 'M', 4)

e = a & a & a & b & b

print('e : %s' % e)
f = getEquiv(e)
print('f : %s' % f)




