# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from verif_msi import *

import os

order = 1
prop = 'tps'
withGlitches = False
dumpCirc = False
checkFunctionality = False
circuitFilename = 'circuit.dot'


def usage():
    print('Usage: %s [options]' % os.path.basename(__file__))
    print('   This script contains a VerifMSI description of a circuit implementing the \'Trichina AND\' function (v1) from [1].')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %s)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference) or \'tps\' (Treshold Probing Security). NI and SNI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \'%s\' (default: %r)' % (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %r)' % checkFunctionality)
    print('')
    print('[1] Trichina, E. (2003). Combinational logic design for AES subbyte transformation on masked data. Cryptology EPrint Archive.')


def trichina_and_v1(*argv):
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
    
    
    if order >= 2:
        print('*** Error: the order of verification (%d) must be less than the number of shares (2)' % (order))
        sys.exit(1)
    
    if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni':
        print('*** Error: Unknown security property: %s' % prop)
        print('    Valid values are: \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference), \'rni\' (Relaxed Non-Interference) and \'tps\' (Treshold Probing Security)')
        sys.exit(1)
 


    a = symbol('a', 'S', 1)
    b = symbol('b', 'S', 1)
    
    if prop == 'tps':
        a0, a1 = getPseudoShares(a, 2)
        b0, b1 = getPseudoShares(b, 2)
    else:
        a0, a1 = getRealShares(a, 2)
        b0, b1 = getRealShares(b, 2)
    
    
    a0 = inputGate(a0)
    a1 = inputGate(a1)
    b0 = inputGate(b0)
    b1 = inputGate(b1)
    
    
    # output s = s0 ^ s1 = a & b
    
    # s0 = a0 & b1 ^ b0 & a1 ^ a0 & b0
    # s1 = a1 & b1
    
    c0 = andGate(a0, b1)
    c1 = andGate(b0, a1)
    c2 = andGate(a0, b0)
    c3 = xorGate(c0, c1)
    s0 = xorGate(c2, c3)
    s1 = andGate(a1, b1)
    
    if checkFunctionality:
        res, v0, v1 = compareExpsWithExev(s0.getSymbExp() ^ s1.getSymbExp(), a & b)
        if res == None:
            print('# functionality (exhaustive evaluation): [OK]')
        else:
            print('# functionality (exhaustive evaluation): [KO]')
            print(res)
    
    if dumpCirc:
        dumpCircuit(circuitFilename, s0, s1)
    
    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, s0, s1)
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = trichina_and_v1(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)


