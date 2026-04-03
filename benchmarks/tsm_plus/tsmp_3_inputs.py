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
    print('   This script contains a VerifMSI description of the TSM+ gadget from [1] with 3 inputs.')
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



def tsmp_3_inputs(*argv):
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


    k1 = symbol("k1", 'S', bitwidth)
    k2 = symbol("k2", 'S', bitwidth)
    k3 = symbol("k3", 'S', bitwidth)
    k10, k11 = getRealShares(k1, 2)
    k20, k21 = getRealShares(k2, 2)
    k30, k31 = getRealShares(k3, 2)

    
    m0 = symbol("m0", 'M', bitwidth)
    m1 = symbol("m1", 'M', bitwidth)
    m2 = symbol("m2", 'M', bitwidth)
    m3 = symbol("m3", 'M', bitwidth)
    m4 = symbol("m4", 'M', bitwidth)
    m5 = symbol("m5", 'M', bitwidth)
    m6 = symbol("m6", 'M', bitwidth)

    x0 = inputGate(k10)
    x1 = inputGate(k11)
    y0 = inputGate(k20)
    y1 = inputGate(k21)
    z0 = inputGate(k30)
    z1 = inputGate(k31)
    r0 = inputGate(m0)
    r1 = inputGate(m1)
    r2 = inputGate(m2)
    r3 = inputGate(m3)
    r4 = inputGate(m4)
    r5 = inputGate(m5)
    r6 = inputGate(m6)

    x1y1 = andGate(x1, y1)
    x0y0 = andGate(x0, y0)
    x1z1 = andGate(x1, z1)
    x0z0 = andGate(x0, z0)
    y1z1 = andGate(y1, z1)
    y0z0 = andGate(y0, z0)
    x1y1z1 = andGate(x1y1, z1)
    x0y0z0 = andGate(x0y0, z0)

    x1_p = xorGate(x1, r0)
    y1_p = xorGate(y1, r1)
    z1_p = xorGate(z1, r2)
    x1y1_p = xorGate(x1y1, r3)
    x1z1_p = xorGate(x1z1, r4)
    y1z1_p = xorGate(y1z1, r5)
    x1y1z1_p = xorGate(x1y1z1, r6)

    x0r5 = andGate(x0, r5)
    y0r4 = andGate(y0, r4)
    z0r3 = andGate(z0, r3)
    x0y0r2 = andGate(x0y0, r2)
    x0z0r1 = andGate(x0z0, r1)
    y0z0r0 = andGate(y0z0, r0)

    fc_part1 = xorGate(x0y0z0, x0r5)
    fc_part2 = xorGate(y0r4, z0r3)
    fc_part3 = xorGate(x0y0r2, x0z0r1)
    fc_part4 = xorGate(y0z0r0, r6)
    fc = xorGate(xorGate(fc_part1, fc_part2), xorGate(fc_part3, fc_part4))

    r_x0 = Register(x0)
    r_y0 = Register(y0)
    r_z0 = Register(z0)
    r_x1y1_p = Register(x1y1_p)
    r_x1z1_p = Register(x1z1_p)
    r_y1z1_p = Register(y1z1_p)
    r_x1_p = Register(x1_p)
    r_y1_p = Register(y1_p)
    r_z1_p = Register(z1_p)
    r_fc = Register(fc)


    x0_y1z1_p = andGate(r_x0, r_y1z1_p)
    y0_x1z1_p = andGate(r_y0, r_x1z1_p)
    z0_x1y1_p = andGate(r_z0, r_x1y1_p)
    x0y0z1_p = andGate(andGate(r_x0, r_y0), r_z1_p)
    x0z0y1_p = andGate(andGate(r_x0, r_z0), r_y1_p)
    y0z0x1_p = andGate(andGate(r_y0, r_z0), r_x1_p)
    f0_part1 = xorGate(x0_y1z1_p, y0_x1z1_p);
    f0_part2 = xorGate(z0_x1y1_p, x0y0z1_p);
    f0_part3 = xorGate(x0z0y1_p, y0z0x1_p);
    

    f0 = xorGate(xorGate(f0_part1, f0_part2), xorGate(f0_part3, r_fc))
    f1 = Register(x1y1z1_p)


    if checkFunctionality:
        res, v0, v1 = compareExpsWithExev(f0.getSymbExp() ^ f1.getSymbExp(), k1 & k2 & k3)
        if res == None:
            print('# functionality (exhaustive evaluation): [OK]')
        else:
            print('# functionality (exhaustive evaluation): [KO]')
            print(res)

    if dumpCirc:
        dumpCircuit('circuit.dot', f0, f1)

    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, f0, f1)
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = tsmp_3_inputs(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)
