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
    print('   This script contains a VerifMSI description of a circuit implementing the logical AND following the GMS scheme with 3 shares from [1].')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %s)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference) or \'tps\' (Treshold Probing Security). NI and SNI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \'%s\' (default: %r)' % (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %r)' % checkFunctionality)
    print('')
    print('[1] Reparaz, O., Bilgin, B., Nikova, S., Gierlichs, B., & Verbauwhede, I. (2015). Consolidating masking schemes. 35th Annual Cryptology Conference, 2015. Springer Berlin Heidelberg.')



def gms_and_3_shares(*argv):
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
    
    
    if order >= 3:
        print('*** Error: the order of verification (%d) must be less than the number of shares (3)' % (order))
        sys.exit(1)
    
    if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni':
        print('*** Error: Unknown security property: %s' % prop)
        print('    Valid values are: \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference), \'rni\' (Relaxed Non-Interference) and \'tps\' (Treshold Probing Security)')
        sys.exit(1)
    
 
    a = symbol('a', 'S', 1)
    b = symbol('b', 'S', 1)
    
    if prop == 'tps':
        a0, a1, a2 = getPseudoShares(a, 3)
        b0, b1, b2 = getPseudoShares(b, 3)
    else:
        a0, a1, a2 = getRealShares(a, 3)
        b0, b1, b2 = getRealShares(b, 3)
    
    z12 = symbol('z12', 'M', 1)
    z13 = symbol('z13', 'M', 1)
    z23 = symbol('z23', 'M', 1)
    
    a0 = inputGate(a0)
    a1 = inputGate(a1)
    a2 = inputGate(a2)
    b0 = inputGate(b0)
    b1 = inputGate(b1)
    b2 = inputGate(b2)
    
    z12 = inputGate(z12)
    z13 = inputGate(z13)
    z23 = inputGate(z23)
    
    
    # Non linear layer
    a0b0 = andGate(a0, b0)
    a0b1 = andGate(a0, b1)
    a0b2 = andGate(a0, b2)
    a1b0 = andGate(a1, b0)
    a1b1 = andGate(a1, b1)
    a1b2 = andGate(a1, b2)
    a2b0 = andGate(a2, b0)
    a2b1 = andGate(a2, b1)
    a2b2 = andGate(a2, b2)
    
    # Linear Layer
    l00 = xorGate(a0b0, a2b0)
    l0 = xorGate(l00, a0b2)
    l10 = xorGate(a1b0, a0b1)
    l1 = xorGate(l10, a1b1)
    l20 = xorGate(a2b1, a1b2)
    l2 = xorGate(l20, a2b2)
    
    # Refreshing Layer
    c00 = xorGate(l0, z12)
    c0 = xorGate(c00, z13)
    c10 = xorGate(l1, z12)
    c1 = xorGate(c10, z23)
    c20 = xorGate(l2, z13)
    c2 = xorGate(c20, z23)
     
     
    if checkFunctionality:
        res, v0, v1 = compareExpsWithExev(c0.getSymbExp() ^ c1.getSymbExp() ^ c2.getSymbExp(), a & b)
        if res == None:
            print('# functionality (exhaustive evaluation): [OK]')
        else:
            print('# functionality (exhaustive evaluation): [KO]')
            print(res)
    
    if dumpCirc:
        dumpCircuit(circuitFilename, c0, c1, c2)
    
    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, c0, c1, c2)
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = gms_and_3_shares(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)




