
from verif_msi import *


a = symbol('a', 'P', 4)
b = symbol('b', 'P', 4)
c = symbol('c', 'P', 4)
d = symbol('d', 'P', 4)
e = symbol('e', 'P', 4)

x = symbol('x', 'S', 4)
y = symbol('y', 'S', 4)
z = symbol('z', 'S', 4)

e = OpNode('+', [a, b, c, a])
f = OpNode('+', [a, a, a, a])

src = OpNode('^', [e, f])



trg = a ^ b ^ c ^ d




addSimpRule(src, trg)

e = (x + x + y + y) ^ (x + x + x + x)
e = simplify(e)

print('e : %s' % e)
f = getEquiv(e)
print('f : %s' % f)




