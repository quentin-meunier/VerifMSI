# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

import sys
import os

nbShares = 3
order = 2
prop = 'ni'
withGlitches = False
withAdditionalRand = False
outfilePrefix = 'isw_and_gen'
outfile = None


def usage():
    print('Usage: %s [options]' % os.path.basename(__file__))
    print('   This script generates a VerifMSI file describing a circuit implementing the logical AND following the ISW scheme.')
    print('Options:')
    print('-f,  --outfile <file>       : Set the name of the generated output file to <file> (default: %s)' % outfile)
    print('-n,  --nb-shares <n>        : Set the number of shares in the scheme to <n> (default: %s)' % nbShares)
    print('-o,  --order <n>            : set the order of the verification to (default: %s)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference), \'pini\' (Probing-Isolating Non-Interference) or \'tps\' (Treshold Probing Security). NI, SNI, RNI and PINI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-r,  --with-rand            : Use an additional random for computing expressions of the form a_i & b_j,')
    print('                              to transform them into ((a_i ^ r) & b_j) ^ (r & b_j) (defaut: %s)' % (withAdditionalRand and 'Yes' or 'No'))
    print('-nr, --with-rand            : Do not use additional random for computing expressions of the form a_i & b_j (default: %s)' % (withAdditionalRand and 'No' or 'Yes'))



def generate_isw_and(*argv):
    global nbShares
    global order
    global prop
    global withGlitches
    global withAdditionalRand
    global outfile

    idx = 0
    while idx < len(argv):
        arg = argv[idx]
        if arg == '-h' or arg == '--help':
            usage()
            sys.exit(0)
        elif arg == '-f' or arg == '--outfile':
            idx += 1
            outfile = argv[idx]
        elif arg == '-n' or arg == '--nb-shares':
            idx += 1
            nbShares = int(argv[idx])
        elif arg == '-o' or arg == '--order':
            idx += 1
            order = int(argv[idx])
        elif arg == '-p' or arg == '--prop':
            idx += 1
            prop = argv[idx]
        elif arg == '-g' or arg == '--with-glitches':
            withGlitches = True
        elif arg == '-ng' or arg == '--without-glitches':
            withGlitches = False
        elif arg == '-r' or arg == '--with-rand':
            withAdditionalRandom = True
        elif arg == '-nr' or arg == '--without-rand':
            withAdditionalRandom = False
        else:
            print('*** Error: unrecognized option: %s' % arg, file = sys.stderr)
            usage()
            sys.exit(1)
        idx += 1
    
    if outfile == None:
        outfile = outfilePrefix + '_%d_shares.py' % nbShares
    
    if order >= nbShares:
        print('*** Error: the order of verification (%d) must be less than the number of shares (%d)' % (order, nbShares))
        sys.exit(1)
    
    if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni' and prop != 'pini':
        print('*** Error: Unknown security property: %s' % prop)
        print('    Valid values are: \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference), \'rni\' (Relaxed Non-Interference), \'pini\' (Probing-Isolating Non-Interference) and \'tps\' (Treshold Probing Security)')
        sys.exit(1)

    nextRandNum = 0
    def getNewRandNum():
        global nextRandNum
        v = nextRandNum
        nextRandNum += 1
        return v


    content = '''# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# File generated by generate_isw_and.py

from verif_msi import *

import os
import sys

'''
    
    content += 'order = %d\n' % order
    content += 'prop = \'%s\'\n' % prop
    content += 'withGlitches = %r\n' % withGlitches
    content += 'dumpCirc = False\n'
    content += 'checkFunctionality = False\n'
    content += 'circuitFilename = \'circuit.dot\'\n'
    content += '\n'
    
    content += '''def usage():
    print('Usage: %%s [options]' %% os.path.basename(__file__))
    print('   This script contains a VerifMSI description of a circuit implementing the logical AND following the ISW scheme with %d shares.')
    print('   This file was generated using the script generate_isw_and.py')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %%d)' %% order)
    print('-p,  --prop                 : Set security property to verify: either \\\'ni\\\' (Non-Interference), \\\'sni\\\' (Strong Non-Interference) \\\'rni\\\' (Relaxed Non-Interference), \\\'pini\\\' (Probing-Isolating Non-Interference) or \\\'tps\\\' (Treshold Probing Security). NI, SNI, RNI and PINI use a share description for the inputs, while TPS uses a secrets + masks description (default: %%s)' %% prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %%s)' %% (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %%s)' %% (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \\\'%%s\\\' (default: %%r)' %% (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %%r)' %% checkFunctionality)
''' % (nbShares)

    content += '\n'
    content += '\n'

    content += '''def isw_and_%d_shares(*argv):
    global order
    global prop
    global withGlitches
    global dumpCirc
    global checkFunctionality

    idx = 0
    while idx < len(argv):
        arg = argv[idx]
        if arg == '-h' or arg == '--help':
            usage()
            sys.exit(0)
        elif arg == '-o' or arg == '--order':
            idx += 1
            order = int(argv[idx])
        elif arg == '-p' or arg == '--prop':
            idx += 1
            prop = argv[idx]
        elif arg == '-g' or arg == '--with-glitches':
            withGlitches = True
        elif arg == '-ng' or arg == '--without-glitches':
            withGlitches = False
        elif arg == '-d' or arg == '--dump-circuit':
            dumpCirc = True
        elif arg == '-c' or arg == '--check-functionality':
            checkFunctionality = True
        else:
            print('*** Error: unrecognized option: %%s' %% arg, file = sys.stderr)
            usage()
            sys.exit(1)
        idx += 1
    
    
    if order >= %d:
        print('*** Error: the order of verification (%%d) must be less than the number of shares (%d)' %% (order))
        sys.exit(1)
    
    if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni' and prop != 'pini':
        print('*** Error: Unknown security property: %%s' %% prop)
        print('    Valid values are: \\\'ni\\\' (Non-Interference), \\\'sni\\\' (Strong Non-Interference), \\\'rni\\\' (Relaxed Non-Interference), \\\'pini\\\' (Probing-Isolating Non-Interference) and \\\'tps\\\' (Treshold Probing Security)')
        sys.exit(1)
    

''' % (nbShares, nbShares, nbShares)


    inputVars = ('a', 'b')
    outputVar = 'c'
    
    content += '    %s = symbol(\'%s\', \'S\', 1)\n' % (inputVars[0], inputVars[0])
    content += '    %s = symbol(\'%s\', \'S\', 1)\n' % (inputVars[1], inputVars[1])
    content += '\n'
    
    
    content += '    if prop == \'tps\':\n'
    for var in inputVars:
        content += '        %s0' % var
        for i in range(1, nbShares):
            content += ', %s%d' % (var, i)
        content += ' = getPseudoShares(%s, %d)' % (var, nbShares)
        content += '\n'
    content += '    else:\n'
    for var in inputVars:
        content += '        %s0' % var
        for i in range(1, nbShares):
            content += ', %s%d' % (var, i)
        content += ' = getRealShares(%s, %d)' % (var, nbShares)
        content += '\n'
    content += '\n'
    
    
    for var in inputVars:
        for sh in range(nbShares):
            content += '    %s%d = inputGate(%s%d)\n' % (var, sh, var, sh)
    content += '\n'
    
    
    for i in range(nbShares - 1):
        for j in range(i + 1, nbShares):
            content += '    z%d_%d = symbol(\'z%d_%d\', \'M\', 1)\n' % (i, j, i, j)
            content += '    z%d_%d = inputGate(z%d_%d)\n' % (i, j, i, j)
            if withAdditionalRand:
                randNum = getNewRandNum()
                content += '    r%d = symbol(\'r%d\', \'M\', 1)\n' % (randNum, randNum)
                content += '    r%d = inputGate(r%d)\n' % (randNum, randNum)
                content += '    %s%d%s%d = xorGate(andGate(xorGate(%s%d, r%d), %s%d), andGate(r%d, %s%d))\n' % (inputVars[0], i, inputVars[1], j, inputVars[0], i, randNum, inputVars[1], j, randNum, inputVars[1], j)
                randNum = getNewRandNum()
                content += '    r%d = symbol(\'r%d\', \'M\', 1)\n' % (randNum, randNum)
                content += '    r%d = inputGate(r%d)\n' % (randNum, randNum)
                content += '    %s%d%s%d = xorGate(andGate(xorGate(%s%d, r%d), %s%d), andGate(r%d, %s%d))\n' % (inputVars[0], j, inputVars[1], i, inputVars[0], j, randNum, inputVars[1], i, randNum, inputVars[1], i)
            else:
                content += '    %s%d%s%d = andGate(%s%d, %s%d)\n' % (inputVars[0], i, inputVars[1], j, inputVars[0], i, inputVars[1], j)
                content += '    %s%d%s%d = andGate(%s%d, %s%d)\n' % (inputVars[0], j, inputVars[1], i, inputVars[0], j, inputVars[1], i)
            content += '    z%d_%d = xorGate(xorGate(z%d_%d, %s%d%s%d), %s%d%s%d)\n' % (j, i, i, j, inputVars[0], i, inputVars[1], j, inputVars[0], j, inputVars[1], i)
    content += '\n'
    
    
    for i in range(nbShares):
        content += '    %s%d = andGate(%s%d, %s%d)\n' % (outputVar, i, inputVars[0], i, inputVars[1], i)
        for j in range(nbShares):
            if i != j:
                content += '    %s%d = xorGate(%s%d, z%d_%d)\n' % (outputVar, i, outputVar, i, i, j)
    
    
    content += '\n'
    content += '    if checkFunctionality:\n'
    content += '        res, v0, v1 = compareExpsWithExev(' + ' ^ '.join(['%s%d.symbExp' % (outputVar, i) for i in range(nbShares)]) + ', %s & %s)\n' % (inputVars[0], inputVars[1])
    content += '        if res == None:\n'
    content += '            print(\'# functionality (exhaustive evaluation): [OK]\')\n'
    content += '        else:\n'
    content += '            print(\'# functionality (exhaustive evaluation): [KO]\')\n'
    content += '            print(res)\n'
    content += '\n'
    
    content += '    if dumpCirc:\n'
    content += '        dumpCircuit(\'circuit.dot\', ' + ', '.join(['%s%d' % (outputVar, i) for i in range(nbShares)]) + ')\n'
    content += '\n'
    
    content += '    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, ' + ', '.join(['%s%d' % (outputVar, i) for i in range(nbShares)]) + ')\n'
    content += '    return nbLeak, nbCheck\n'
    content += '\n'
    content += '\n'
 
    content += '''if __name__ == '__main__':
    nbLeak, nbCheck = isw_and_%d_shares(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %%d' %% nbCheck)
    print('# Total Nb. of potential leakages found: %%d' %% nbLeak)

''' % (nbShares)
    
    f = open(outfile, 'w')
    f.write(content)
    f.close()


if __name__ == '__main__':
    generate_isw_and(*sys.argv[1:])


