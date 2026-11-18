
from verif_msi import *


a = symbol('a', 'P', 4)
b = symbol('b', 'P', 4)
c = symbol('c', 'P', 4)
d = symbol('d', 'P', 4)

x = symbol('x', 'S', 4)
y = symbol('y', 'S', 4)
z = symbol('z', 'S', 4)


src = a & (d ^ (b & c))
src = simplify(src)

trg = a ^ b ^ c
print('# src : %s' % src)

addSimpRule(src, trg)

e = x & (x ^ (y & z))
print('# e : %s' % e)
e = simplify(e)
# a -> x
# b -> y
# c -> z
# d -> x
# e -> z

print('# e : %s' % e)






