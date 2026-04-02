# Copyright (C) 2026, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author: Quentin L. Meunier, Lucie Chauvière


from verif_msi import *

import os
import sys

order = 1
prop = 'ni'
withGlitches = True
dumpCirc = False
checkFunctionality = False
circuitFilename = 'circuit.dot'
bitwidth = 1


def usage():
    print('Usage: %s [options]' % os.path.basename(__file__))
    print('   This script contains a VerifMSI description of the TSM gadget from [1].')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %d)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference), \'pini\' (Probing-Isolating Non-Interference) or \'tps\' (Treshold Probing Security). NI, SNI, RNI and PINI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \'%s\' (default: %r)' % (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %r)' % checkFunctionality)
    print('')
    print('[1] H. Rahimi & A. Moradi (2026). TSM+ and OTSM-Correct Application of Time Sharing Masking in Round-Based Designs. Cryptology ePrint Archive. https://eprint.iacr.org/2026/004')



def getShares(s, nbShares):
    if (prop == 'tps'):
        return getPseudoShares(s, nbShares)
    else:
        return getRealShares(s, nbShares)

def tsm():

    k1 = symbol("k1", 'S', bitwidth)
    k2 = symbol("k2", 'S', bitwidth)

    k10, k11 = getRealShares(k1, 2)
    k20, k21 = getRealShares(k2, 2)

    z0 = symbol("z0", 'M', bitwidth)
    z1 = symbol("z1", 'M', bitwidth)
    z2 = symbol("z2", 'M', bitwidth)
    z3 = symbol("z3", 'M', bitwidth)
    z4 = symbol("z4", 'M', bitwidth)

    x0 = inputGate(k10)
    x1 = inputGate(k11)
    y0 = inputGate(k20)
    y1 = inputGate(k21)

    r0 = inputGate(z0)
    r1 = inputGate(z1)
    r2 = inputGate(z2)
    r3 = inputGate(z3)
    r4 = inputGate(z4)
    
    x0_p = xorGate(x0, r3)
    x1_p = xorGate(x1, r3)
    y0_p = xorGate(y0, r4)
    y1_p = xorGate(y1, r4)

    r_r0 = Register(r0)
    r_r1 = Register(r1)
    r_r2 = Register(r2)
    r_y1_p = Register(y1_p)
    r_x1_p = Register(x1_p)

    x0y0_p = andGate(x0_p, y0_p)
    r0x0y0_p = xorGate(x0y0_p, r0)
    r_r0x0y0_p = Register(r0x0y0_p)
    r_r1x0_p = Register(xorGate(x0_p, r1))
    r_r2y0_p = Register(xorGate(y0_p, r2))
    r1x0y1_p = andGate(r_r1x0_p, r_y1_p)
    r2y0x1_p = andGate(r_r2y0_p, r_x1_p)
    
    r1y1_p = andGate(r_r1, r_y1_p)
    r2x1_p = andGate(r_r2, r_x1_p)
    x1y1_p = andGate(r_x1_p, r_y1_p)

    f0 = xorGate(xorGate(r_r0x0y0_p,r1x0y1_p ), r2y0x1_p)
    f1 = xorGate(xorGate(r_r0, r1y1_p), xorGate(r2x1_p, x1y1_p))
    
    

    if checkFunctionality:
        res, v0, v1 = compareExpsWithExev(f0.getSymbExp() ^ f1.getSymbExp(), k1 & k2)
        if res == None:
            print('# functionality (exhaustive evaluation): [OK]')
        else:
            print('# functionality (exhaustive evaluation): [KO]')
            print(res)

    if dumpCirc:
        dumpCircuit('circuit.dot', f0, f1)

    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, f0, f1)
    return nbLeak, nbCheck




def main(*argv):
    global order
    global prop
    global withGlitches
    global dumpCirc
    global checkFunctionality
    global bitwidth

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
    
    
    if order >= 2:
        print("*** Error: the order of verification should be 1 for this gadget")
        sys.exit(1)
    
    if prop != 'ni' and prop != 'sni' and prop != 'tps' and prop != 'rni' and prop != 'pini' and prop != 'opini':
        print('*** Error: Unknown security property: %s' % prop)
        print('    Valid values are: \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference), \'rni\' (Relaxed Non-Interference), \'pini\' (Probing-Isolating Non-Interference), \'opini\' (Output-PINI) and \'tps\' (Treshold Probing Security)')
        sys.exit(1)
    
    nbLeak, nbCheck = tsm()
    return nbLeak, nbCheck




nbLeak, nbCheck = main()
print('# Total Nb. of expressions analysed: %d' % nbCheck)
print('# Total Nb. of potential leakages found: %d' % nbLeak)


