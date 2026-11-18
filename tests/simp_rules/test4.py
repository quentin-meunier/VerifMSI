
from verif_msi import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)
z = symbol('z', 'P', 8)

orig = OpNode('+', [a, b, c, d, a])
#symbInOrig = [d, c, b, a, a]
exp = OpNode('+', [x, x, y, y, z])

addSimpRule(orig, a ^ b)


print('exp: %s' % exp)
f = getEquiv(exp)



