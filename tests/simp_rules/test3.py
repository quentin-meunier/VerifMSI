
from verif_msi import *


a = symbol('a', 'P', 4)
b = symbol('b', 'P', 4)
c = symbol('c', 'P', 4)
d = symbol('d', 'P', 4)
e = symbol('e', 'P', 4)

x = symbol('x', 'S', 4)
y = symbol('y', 'S', 4)
z = symbol('z', 'S', 4)

src0 = OpNode('+', [a, b, c, d, a]) 
trg0 = a ^ b ^ c ^ d


addSimpRule(src0, trg0)

e = x + x + y + y + z
e = simplify(e)

print('e : %s' % e)
f = getEquiv(e)
print('f : %s' % f)




