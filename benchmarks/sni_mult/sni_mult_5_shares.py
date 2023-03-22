# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from verif_msi import *

import os
import sys

order = 4
prop = 'sni'
withGlitches = False
dumpCirc = False
checkFunctionality = False
circuitFilename = 'circuit.dot'


def usage():
    print('Usage: %s [options]' % os.path.basename(__file__))
    print('   This script contains a VerifMSI description of a circuit implementing the \'SNI Mult\' algorithm [?] with 5 shares.')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %s)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference) or \'tps\' (Treshold Probing Security). NI and SNI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \'%s\' (default: %r)' % (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %r)' % checkFunctionality)


def sni_mult_5_shares(*argv):
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
    
    r0 = symbol('r0', 'M', 1)
    r1 = symbol('r1', 'M', 1)
    r2 = symbol('r2', 'M', 1)
    r3 = symbol('r3', 'M', 1)
    r4 = symbol('r4', 'M', 1)
    r20 = symbol('r20', 'M', 1)
    r21 = symbol('r21', 'M', 1)
    r22 = symbol('r22', 'M', 1)
    r23 = symbol('r23', 'M', 1)
    r24 = symbol('r24', 'M', 1)
    
    r0 = inputGate(r0)
    r1 = inputGate(r1)
    r2 = inputGate(r2)
    r3 = inputGate(r3)
    r4 = inputGate(r4)
    r20 = inputGate(r20)
    r21 = inputGate(r21)
    r22 = inputGate(r22)
    r23 = inputGate(r23)
    r24 = inputGate(r24)
    
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
    
    alpha_0_0 = a0b0
    alpha_0_1 = xorGate(a0b1, a1b0)
    alpha_0_2 = xorGate(a0b2, a2b0)
    alpha_0_3 = xorGate(a0b3, a3b0)
    alpha_0_4 = xorGate(a0b4, a4b0)
    alpha_1_1 = a1b1
    alpha_1_2 = xorGate(a1b2, a2b1)
    alpha_1_3 = xorGate(a1b3, a3b1)
    alpha_1_4 = xorGate(a1b4, a4b1)
    alpha_2_2 = a2b2
    alpha_2_3 = xorGate(a2b3, a3b2)
    alpha_2_4 = xorGate(a2b4, a4b2)
    alpha_3_3 = a3b3
    alpha_3_4 = xorGate(a3b4, a4b3)
    alpha_4_4 = a4b4
    
    c0 = alpha_0_0
    c1 = alpha_1_1
    c2 = alpha_2_2
    c3 = alpha_3_3
    c4 = alpha_4_4
    
    c0 = xorGate(c0, r0)
    c0 = xorGate(c0, alpha_0_1)
    c1 = xorGate(c1, r1)
    c1 = xorGate(c1, alpha_1_2)
    c2 = xorGate(c2, r2)
    c2 = xorGate(c2, alpha_2_3)
    c3 = xorGate(c3, r3)
    c3 = xorGate(c3, alpha_3_4)
    c4 = xorGate(c4, r4)
    c4 = xorGate(c4, alpha_0_4)
    c0 = xorGate(c0, r1)
    c0 = xorGate(c0, alpha_0_2)
    c1 = xorGate(c1, r2)
    c1 = xorGate(c1, alpha_1_3)
    c2 = xorGate(c2, r3)
    c2 = xorGate(c2, alpha_2_4)
    c3 = xorGate(c3, r4)
    c3 = xorGate(c3, alpha_0_3)
    c4 = xorGate(c4, r0)
    c4 = xorGate(c4, alpha_1_4)
    
    c0 = xorGate(c0, r20)
    c0 = xorGate(c0, r24)
    c1 = xorGate(c1, r21)
    c1 = xorGate(c1, r20)
    c2 = xorGate(c2, r22)
    c2 = xorGate(c2, r21)
    c3 = xorGate(c3, r23)
    c3 = xorGate(c3, r22)
    c4 = xorGate(c4, r24)
    c4 = xorGate(c4, r23)


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
    nbLeak, nbCheck = sni_mult_5_shares(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)


