# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from verif_msi import *

import os
import sys

order = 5
prop = 'sni'
withGlitches = False
dumpCirc = False
checkFunctionality = False
circuitFilename = 'circuit.dot'


def usage():
    print('Usage: %s [options]' % os.path.basename(__file__))
    print('   This script contains a VerifMSI description of a circuit implementing the \'SNI Mult\' algorithm [1] with 6 shares.')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %d)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference), \'pini\' (Probing-Isolating Non-Interference) or \'tps\' (Treshold Probing Security). NI, SNI, RNI and PINI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \'%s\' (default: %r)' % (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %r)' % checkFunctionality)
    print('')
    print('[1] Bordes, N., & Karpman, P. (2021). Fast verification of masking schemes in characteristic two. 40th Annual International Conference on the Theory and Applications of Cryptographic Techniques, 2021. Springer International Publishing.')


def sni_mult_6_shares(*argv):
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
            print('*** Error: unrecognized option: %s' % arg, file = sys.stderr)
            usage()
            sys.exit(1)
        idx += 1
    
    
    if order >= 6:
        print('*** Error: the order of verification (%d) must be less than the number of shares (6)' % (order))
        sys.exit(1)
    
    if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni' and prop != 'pini':
        print('*** Error: Unknown security property: %s' % prop)
        print('    Valid values are: \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference), \'rni\' (Relaxed Non-Interference), \'pini\' (Probing-Isolating Non-Interference) and \'tps\' (Treshold Probing Security)')
        sys.exit(1)


    a = symbol('a', 'S', 1)
    b = symbol('b', 'S', 1)

    if prop == 'tps':
        a0, a1, a2, a3, a4, a5 = getPseudoShares(a, 6)
        b0, b1, b2, b3, b4, b5 = getPseudoShares(b, 6)
    else:
        a0, a1, a2, a3, a4, a5 = getRealShares(a, 6)
        b0, b1, b2, b3, b4, b5 = getRealShares(b, 6)

    a0 = inputGate(a0)
    a1 = inputGate(a1)
    a2 = inputGate(a2)
    a3 = inputGate(a3)
    a4 = inputGate(a4)
    a5 = inputGate(a5)
    b0 = inputGate(b0)
    b1 = inputGate(b1)
    b2 = inputGate(b2)
    b3 = inputGate(b3)
    b4 = inputGate(b4)
    b5 = inputGate(b5)

    r0 = symbol('r0', 'M', 1)
    r1 = symbol('r1', 'M', 1)
    r2 = symbol('r2', 'M', 1)
    r3 = symbol('r3', 'M', 1)
    r4 = symbol('r4', 'M', 1)
    r5 = symbol('r5', 'M', 1)
    r6 = symbol('r6', 'M', 1)
    r7 = symbol('r7', 'M', 1)
    r8 = symbol('r8', 'M', 1)
    r9 = symbol('r9', 'M', 1)
    r20 = symbol('r20', 'M', 1)
    r21 = symbol('r21', 'M', 1)
    
    r0 = inputGate(r0)
    r1 = inputGate(r1)
    r2 = inputGate(r2)
    r3 = inputGate(r3)
    r4 = inputGate(r4)
    r5 = inputGate(r5)
    r6 = inputGate(r6)
    r7 = inputGate(r7)
    r8 = inputGate(r8)
    r9 = inputGate(r9)
    r20 = inputGate(r20)
    r21 = inputGate(r21)
    
    a0b0 = andGate(a0, b0)
    a0b1 = andGate(a0, b1)
    a0b2 = andGate(a0, b2)
    a0b3 = andGate(a0, b3)
    a0b4 = andGate(a0, b4)
    a0b5 = andGate(a0, b5)
    a1b0 = andGate(a1, b0)
    a1b1 = andGate(a1, b1)
    a1b2 = andGate(a1, b2)
    a1b3 = andGate(a1, b3)
    a1b4 = andGate(a1, b4)
    a1b5 = andGate(a1, b5)
    a2b0 = andGate(a2, b0)
    a2b1 = andGate(a2, b1)
    a2b2 = andGate(a2, b2)
    a2b3 = andGate(a2, b3)
    a2b4 = andGate(a2, b4)
    a2b5 = andGate(a2, b5)
    a3b0 = andGate(a3, b0)
    a3b1 = andGate(a3, b1)
    a3b2 = andGate(a3, b2)
    a3b3 = andGate(a3, b3)
    a3b4 = andGate(a3, b4)
    a3b5 = andGate(a3, b5)
    a4b0 = andGate(a4, b0)
    a4b1 = andGate(a4, b1)
    a4b2 = andGate(a4, b2)
    a4b3 = andGate(a4, b3)
    a4b4 = andGate(a4, b4)
    a4b5 = andGate(a4, b5)
    a5b0 = andGate(a5, b0)
    a5b1 = andGate(a5, b1)
    a5b2 = andGate(a5, b2)
    a5b3 = andGate(a5, b3)
    a5b4 = andGate(a5, b4)
    a5b5 = andGate(a5, b5)

    alpha_0_0 = a0b0
    alpha_1_1 = a1b1
    alpha_2_2 = a2b2
    alpha_3_3 = a3b3
    alpha_4_4 = a4b4
    alpha_5_5 = a5b5

    c0 = alpha_0_0
    c1 = alpha_1_1
    c2 = alpha_2_2
    c3 = alpha_3_3
    c4 = alpha_4_4
    c5 = alpha_5_5

    c0 = xorGate(c0, r0)
    c0 = xorGate(c0, a0b1) # alpha_0_1
    c0 = xorGate(c0, a1b0)
    c1 = xorGate(c1, r1)
    c1 = xorGate(c1, a1b2) # alpha_1_2
    c1 = xorGate(c1, a2b1)
    c2 = xorGate(c2, r2)
    c2 = xorGate(c2, a2b3) # alpha_2_3
    c2 = xorGate(c2, a3b2)
    c3 = xorGate(c3, r3)
    c3 = xorGate(c3, a3b4) # alpha_3_4
    c3 = xorGate(c3, a4b3)
    c4 = xorGate(c4, r4)
    c4 = xorGate(c4, a4b5) # alpha_4_5
    c4 = xorGate(c4, a5b4)
    c5 = xorGate(c5, r5)
    c5 = xorGate(c5, a0b5) # alpha_0_5
    c5 = xorGate(c5, a5b0)
    c0 = xorGate(c0, r1)
    c0 = xorGate(c0, a0b2) # alpha_0_2
    c0 = xorGate(c0, a2b0)
    c1 = xorGate(c1, r2)
    c1 = xorGate(c1, a1b3) # alpha_1_3
    c1 = xorGate(c1, a3b1)
    c2 = xorGate(c2, r3)
    c2 = xorGate(c2, a2b4) # alpha_2_4
    c2 = xorGate(c2, a4b2)
    c3 = xorGate(c3, r4)
    c3 = xorGate(c3, a3b5) # alpha_3_5
    c3 = xorGate(c3, a5b3)
    c4 = xorGate(c4, r5)
    c4 = xorGate(c4, a0b4) # alpha_0_4
    c4 = xorGate(c4, a4b0)
    c5 = xorGate(c5, r0)
    c5 = xorGate(c5, a1b5) # alpha_1_5
    c5 = xorGate(c5, a5b1)
    c0 = xorGate(c0, r6)
    c0 = xorGate(c0, a0b3) # alpha_0_3
    c0 = xorGate(c0, a3b0)
    c1 = xorGate(c1, r7)
    c1 = xorGate(c1, a1b4) # alpha_1_4
    c1 = xorGate(c1, a4b1)
    c2 = xorGate(c2, r8)
    c2 = xorGate(c2, a2b5) # alpha_2_5
    c2 = xorGate(c2, a5b2)
    c3 = xorGate(c3, r9)

    c0 = xorGate(c0, r7)
    c0 = xorGate(c0, r20)
    c1 = xorGate(c1, r8)
    c1 = xorGate(c1, r21)
    c2 = xorGate(c2, r9)
    c3 = xorGate(c3, r6)
    c4 = xorGate(c4, r20)
    c5 = xorGate(c5, r21)

    if checkFunctionality:
        res, v0, v1 = compareExpsWithRandev(c0.getSymbExp() ^ c1.getSymbExp() ^ c2.getSymbExp() ^ c3.getSymbExp() ^ c4.getSymbExp() ^ c5.getSymbExp(), a & b, 100000)
        if res == None:
            print('# functionality (random evaluation): [OK]')
        else:
            print('# functionality (random evaluation): [KO]')
            print(res)

    if dumpCirc:
        dumpCircuit(circuitFilename, c0, c1, c2, c3, c4, c5)

    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, c0, c1, c2, c3, c4, c5)
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = sni_mult_6_shares(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)



