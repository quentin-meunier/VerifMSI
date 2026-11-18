
from verif_msi import *


a = symbol('a', 'P', 4)
b = symbol('b', 'P', 4)
c = symbol('c', 'P', 4)
d = symbol('d', 'P', 4)
e = symbol('e', 'P', 4)

x = symbol('x', 'S', 4)
y = symbol('y', 'S', 4)
z = symbol('z', 'S', 4)


src = a + b + (a & (b ^ (d & e))) + a + c + (a & (d ^ (b & c)))
src = simplify(src)

trg = a ^ b ^ c
print('# src : %s' % src)

addSimpRule(src, trg)

e   = x + y + (x & (y ^ (x & z))) + z + x + (x & (x ^ (y & z)))
e = simplify(e)
# a -> x
# b -> y
# c -> z
# d -> x
# e -> z




print('# e : %s' % e)
f = getEquiv(e)
print('# f : %s' % f)




