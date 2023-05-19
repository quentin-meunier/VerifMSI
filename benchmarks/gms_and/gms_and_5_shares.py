# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from verif_msi import *

import os

order = 2
prop = 'tps'
withGlitches = False
dumpCirc = False
checkFunctionality = False
circuitFilename = 'circuit.dot'


def usage():
    print('Usage: %s [options]' % os.path.basename(__file__))
    print('   This script contains a VerifMSI description of a circuit implementing the logical AND following the GMS scheme with 5 shares from [1].')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %s)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference) or \'tps\' (Treshold Probing Security). NI and SNI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \'%s\' (default: %r)' % (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %r)' % checkFunctionality)
    print('')
    print('[1] Reparaz, O., Bilgin, B., Nikova, S., Gierlichs, B., & Verbauwhede, I. (2015). Consolidating masking schemes. 35th Annual Cryptology Conference, 2015. Springer Berlin Heidelberg.')


def gms_and_5_shares(*argv):
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
            exit(1)
        idx += 1
    
    
    if order >= 5:
        print('*** Error: the order of verification (%d) must be less than the number of shares (5)' % (order))
        sys.exit(1)
    
    if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni':
        print('*** Error: Unknown security property: %s' % prop)
        print('    Valid values are: \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference), \'rni\' (Relaxed Non-Interference) and \'tps\' (Treshold Probing Security)')
        sys.exit(1)
 

    a = symbol('a', 'S', 1)
    b = symbol('b', 'S', 1)
    
    if prop == 'tps':
        a0, a1, a2, a3, a4 = getPseudoShares(a, 5)
        b0, b1, b2, b3, b4 = getPseudoShares(b, 5)
    else:
        a0, a1, a2, a3, a4 = getRealShares(a, 5)
        b0, b1, b2, b3, b4 = getRealShares(b, 5)
    
    z12 = symbol('z12', 'M', 1)
    z13 = symbol('z13', 'M', 1)
    z14 = symbol('z14', 'M', 1)
    z15 = symbol('z15', 'M', 1)
    z23 = symbol('z23', 'M', 1)
    z24 = symbol('z24', 'M', 1)
    z25 = symbol('z25', 'M', 1)
    z34 = symbol('z34', 'M', 1)
    z35 = symbol('z35', 'M', 1)
    z45 = symbol('z45', 'M', 1)
    
    a0 = inputGate(a0)
    a1 = inputGate(a1)
    a2 = inputGate(a2)
    a3 = inputGate(a3)
    a4 = inputGate(a4)
    b0 = inputGate(b0)
    b1 = inputGate(b1)
    b2 = inputGate(b2)
    b3 = inputGate(b3)
    b4 = inputGate(b4)
    
    z12 = inputGate(z12)
    z13 = inputGate(z13)
    z14 = inputGate(z14)
    z15 = inputGate(z15)
    z23 = inputGate(z23)
    z24 = inputGate(z24)
    z25 = inputGate(z25)
    z34 = inputGate(z34)
    z35 = inputGate(z35)
    z45 = inputGate(z45)
    
    
    # Non linear layer
    a0b0 = andGate(a0, b0)
    a0b1 = andGate(a0, b1)
    a0b2 = andGate(a0, b2)
    a0b3 = andGate(a0, b3)
    a0b4 = andGate(a0, b4)
    a1b0 = andGate(a1, b0)
    a1b1 = andGate(a1, b1)
    a1b2 = andGate(a1, b2)
    a1b3 = andGate(a1, b3)
    a1b4 = andGate(a1, b4)
    a2b0 = andGate(a2, b0)
    a2b1 = andGate(a2, b1)
    a2b2 = andGate(a2, b2)
    a2b3 = andGate(a2, b3)
    a2b4 = andGate(a2, b4)
    a3b0 = andGate(a3, b0)
    a3b1 = andGate(a3, b1)
    a3b2 = andGate(a3, b2)
    a3b3 = andGate(a3, b3)
    a3b4 = andGate(a3, b4)
    a4b0 = andGate(a4, b0)
    a4b1 = andGate(a4, b1)
    a4b2 = andGate(a4, b2)
    a4b3 = andGate(a4, b3)
    a4b4 = andGate(a4, b4)
    
    
    # Linear Layer
    l0 = xorGate(a1b3, a3b1)
    l1i = xorGate(a1b1, a0b1)
    l1 = xorGate(l1i, a1b0)
    l2 = xorGate(a3b4, a4b3)
    l3i = xorGate(a0b4, a4b0)
    l3 = xorGate(l3i, a0b0)
    l4 = xorGate(a2b4, a4b2)
    l5i = xorGate(a4b4, a1b4)
    l5 = xorGate(l5i, a4b1)
    l6 = xorGate(a2b3, a3b2)
    l7i = xorGate(a3b3, a0b3)
    l7 = xorGate(l7i, a3b0)
    l8 = xorGate(a1b2, a2b1)
    l9i = xorGate(a2b2, a0b2)
    l9 = xorGate(l9i, a2b0)
    
    
    # Refreshing Layer
    c00i = xorGate(l0, z45)
    c00 = xorGate(c00i, z12)
    c01i = xorGate(l1, z12)
    c01 = xorGate(c01i, z13)
    c10i = xorGate(l2, z13)
    c10 = xorGate(c10i, z14)
    c11i = xorGate(l3, z14)
    c11 = xorGate(c11i, z15)
    c20i = xorGate(l4, z15)
    c20 = xorGate(c20i, z23)
    c21i = xorGate(l5, z23)
    c21 = xorGate(c21i, z24)
    c30i = xorGate(l6, z24)
    c30 = xorGate(c30i, z25)
    c31i = xorGate(l7, z25)
    c31 = xorGate(c31i, z34)
    c40i = xorGate(l8, z34)
    c40 = xorGate(c40i, z35)
    c41i = xorGate(l9, z35)
    c41 = xorGate(c41i, z45)
    
    
    # Compression Layer
    c0 = xorGate(c00, c01)
    c1 = xorGate(c10, c11)
    c2 = xorGate(c20, c21)
    c3 = xorGate(c30, c31)
    c4 = xorGate(c40, c41)
    
     
    
    if checkFunctionality:
        res, v0, v1 = compareExpsWithExev(c0.symbExp ^ c1.symbExp ^ c2.symbExp ^ c3.symbExp ^ c4.symbExp, a & b)
        if res == None:
            print('# functionality (exhaustive evaluation): [OK]')
        else:
            print('# functionality (exhaustive evaluation): [KO]')
            print(res)
    
    if dumpCirc:
        dumpCircuit(circuitFilename, c0, c1, c2, c3, c4)
    
    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, c0, c1, c2, c3, c4)
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = gms_and_5_shares(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)



