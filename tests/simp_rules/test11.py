
from verif_msi import *


a = symbol('a', 'P', 1)
b = symbol('b', 'P', 1)
c = symbol('c', 'P', 1)

x = symbol('x', 'S', 1)
y = symbol('y', 'S', 1)
r = symbol('r', 'M', 1)


ruleSrc = simplify(((a ^ c) & b) ^ ((constant(1, 1) ^ b) & c))
ruleDst = simplify((a & b) ^ c)
addSimpRule(ruleSrc, ruleDst)


e = ((x ^ r) & y) ^ ((constant(1, 1) ^ y) & r)
print('# e : %s' % e)

e = simplify(e)
print('# e : %s' % e)






