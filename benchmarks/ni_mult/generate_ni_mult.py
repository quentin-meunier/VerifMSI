#!/usr/bin/python

import sys
import os

nbShares = 5
order = 4
prop = 'ni'
withGlitches = False
outfile = 'sni_mult_gen_5_sh.py'



def usage(argv):
    print('Usage: %s [options]' % argv[0])
    print('   This script generates a VerifMSI file describing a circuit implementing the logical AND following the ISW scheme.')
    print('Options:')
    print('-f,  --outfile <file>       : Set the name of the generated output file to <file> (default: %s)' % outfile)
    print('-n,  --nb-shares <n>        : Set the number of shares in the scheme to <n> (default: %s)' % nbShares)
    print('-o,  --order <n>            : set the order of the verification to (default: %s)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference) or \'tps\' (Treshold Probing Security). NI and SNI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))


idx = 1
while idx < len(sys.argv):
    arg = sys.argv[idx]
    if arg == '-h' or arg == '--help':
        usage(sys.argv)
        sys.exit(0)
    elif arg == '-f' or arg == '--outfile':
        idx += 1
        outfile = sys.argv[idx]
    elif arg == '-n' or arg == '--nb-shares':
        idx += 1
        nbShares = int(sys.argv[idx])
    elif arg == '-o' or arg == '--order':
        idx += 1
        order = int(sys.argv[idx])
    elif arg == '-p' or arg == '--prop':
        idx += 1
        prop = sys.argv[idx]
    elif arg == '-g' or arg == '--with-glitches':
        withGlitches = True
    elif arg == '-ng' or arg == '--without-glitches':
        withGlitches = False
    else:
        print('*** Error: unrecognized option: %s' % arg, file = sys.stderr)
        usage(sys.argv)
        exit(1)
    idx += 1


if order >= nbShares:
    print('*** Error: the order of verification (%d) must be less than the number of shares (%d)' % (order, nbShares))
    sys.exit(1)

if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni':
    print('*** Error: Unknown security property: %s' % prop)
    print('    Valid values are: \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference), \'rni\' (Relaxed Non-Interference) and \'tps\' (Treshold Probing Security)')
    sys.exit(1)



nextRandNum = 0
def getNewRandNum():
    global nextRandNum
    v = nextRandNum
    nextRandNum += 1
    return v


content = '''



'''

content += 'order = %d\n' % order
content += 'prop = \'%s\'\n' % prop
content += 'withGlitches = %r\n' % withGlitches
content += 'dumpCirc = False\n'
content += 'checkFunctionality = False\n'
content += '\n'

inputVars = ('a', 'b')
outputVar = 'c'

content += '%s = symbol(\'%s\', \'S\', 1)\n' % (inputVars[0], inputVars[0])
content += '%s = symbol(\'%s\', \'S\', 1)\n' % (inputVars[1], inputVars[1])
content += '\n'


content += 'if prop == \'tps\':\n'
for var in inputVars:
    content += '    %s0' % var
    for i in range(1, nbShares):
        content += ', %s%d' % (var, i)
    content += ' = getPseudoShares(%s, %d)' % (var, nbShares)
    content += '\n'
content += 'else:\n'
for var in inputVars:
    content += '    %s0' % var
    for i in range(1, nbShares):
        content += ', %s%d' % (var, i)
    content += ' = getRealShares(%s, %d)' % (var, nbShares)
    content += '\n'
content += '\n'


for var in inputVars:
    for sh in range(nbShares):
        content += '%s%d = inputGate(%s%d)\n' % (var, sh, var, sh)
content += '\n'

initContent = content

content = ''
for i in range(nbShares):
    for j in range(nbShares):
        content += '%s%d%s%d = andGate(%s%d, %s%d)\n' % (inputVars[0], i, inputVars[1], j, inputVars[0], i, inputVars[1], j)
content += '\n'

s = set()
for i in range(nbShares):
    content += 'alpha_%d_%d = %s%d%s%d\n' % (i, i, inputVars[0], i, inputVars[1], i)
    for j in range(i + 1, nbShares):
        content += 'alpha_%d_%d = xorGate(%s%d%s%d, %s%d%s%d)\n' % (i, j, inputVars[0], i, inputVars[1], j, inputVars[0], j, inputVars[1], i)
        s.add('%d_%d' % (i, j))
content += '\n'

for i in range(nbShares):
    content += 'c%d = alpha_%d_%d\n' % (i, i, i)
content += '\n'


rp = set() # R'
randoms = set()
j = 1
while len(s) != 0:
    for i in range(nbShares):
        if j % 2 == 1:
            idx = (j - 1) // 2 * nbShares + i
            content += 'c%d = xorGate(c%d, r%d)\n' % (i, i, idx)
            rp.add(idx)
            randoms.add(idx)
        else:
            idx = (j - 2) // 2 * nbShares + (i + 1) % nbShares
            content += 'c%d = xorGate(c%d, r%d)\n' % (i, i, idx)
            rp.remove(idx)
            randoms.add(idx)
        if len(s) != 0:
            u = min(i, (i + j) % nbShares)
            v = max(i, (i + j) % nbShares)
            content += 'c%d = xorGate(c%d, alpha_%d_%d)\n' % (i, i, u, v)
            s.remove('%d_%d' % (u, v))
            #s.remove('%d_%d' % (i, (i + j) % nbShares))

                #print('%d_%d key error' % (i, (i + j) % nbShares))
                #print('%s' % content)
                #sys.exit(0)
        else:
            break
    j += 1
content += '\n'

k = len(rp)
for i in range(nbShares):
    try:
        content += '%s%d = xorGate(c%d, r%d)\n' % (outputVar, i, i, (j - 1) // 2 * nbShares + (i + 1) % k)
    except:
        continue
        #print('k: %d' % k)
        #print('%s' % initContent)
        #print('%s' % content)
        #sys.exit(0)


# Randoms declaration and input gates
randContent = ''
for i in sorted(randoms):
    randContent += 'r%d = symbol(\'r%d\', \'M\', 1)\n' % (i, i)
randContent += '\n'
for i in sorted(randoms):
    randContent += 'r%d = inputGate(r%d)\n' % (i, i)
randContent += '\n'



content += '\n'
content += 'if checkFunctionality:\n'
content += '    res, v0, v1 = compareExpsWithExev(' + ' ^ '.join(['%s%d.symbExp' % (outputVar, i) for i in range(nbShares)]) + ', %s & %s)\n' % (inputVars[0], inputVars[1])
content += '    if res == None:\n'
content += '        print(\'# functionality (exhaustive evaluation): [OK]\')\n'
content += '    else:\n'
content += '        print(\'# functionality (exhaustive evaluation): [KO]\')\n'
content += '        print(res)\n'
content += '\n'

content += 'if dumpCirc:\n'
content += '    dumpCircuit(\'circuit.dot\', ' + ', '.join(['%s%d' % (outputVar, i) for i in range(nbShares)]) + ')\n'
content += '\n'

content += 'checkSecurity(order, withGlitches, prop, ' + ', '.join(['%s%d' % (outputVar, i) for i in range(nbShares)]) + ')\n'
content += '\n'


f = open(outfile, 'w')
f.write(initContent)
f.write(randContent)
f.write(content)
f.close()


