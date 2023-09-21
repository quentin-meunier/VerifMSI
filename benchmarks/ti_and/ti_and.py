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
    print('   This script contains a VerifMSI description of a circuit implementing the \'Threshold Implementation\' (unbalanced, with 3 shares) from [1].')
    print('Options:')
    print('-o,  --order <n>            : Set the order of the verification to (default: %s)' % order)
    print('-p,  --prop                 : Set security property to verify: either \'ni\' (Non-Interference), \'sni\' (Strong Non-Interference) \'rni\' (Relaxed Non-Interference) or \'tps\' (Treshold Probing Security). NI and SNI use a share description for the inputs, while TPS uses a secrets + masks description (default: %s)' % prop)
    print('-g,  --with-glitches        : Consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'Yes' or 'No'))
    print('-ng, --without-glitches     : Do not consider glitch propagation throughout gates (defaut: %s)' % (withGlitches and 'No' or 'Yes'))
    print('-d, --dump-circuit          : Dump the circuit in dot format in a file named \'%s\' (default: %r)' % (circuitFilename, dumpCircuit))
    print('-c, --check-functionality   : Check the circuit functionality via exhaustive evaluation (default: %r)' % checkFunctionality)
    print('')
    print('[1] Nikova, S., Rechberger, C., & Rijmen, V. (2006). Threshold implementations against side-channel attacks and glitches. In ICICS (Vol. 4307, pp. 529-545).')


def ti_and(*argv):
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
 

    x = symbol('x', 'S', 1)
    y = symbol('y', 'S', 1)
    
    if prop == 'tps':
        x0, x1, x2 = getPseudoShares(x, 3)
        y0, y1, y2 = getPseudoShares(y, 3)
    else:
        x0, x1, x2 = getRealShares(x, 3)
        y0, y1, y2 = getRealShares(y, 3)
    
    
    x0 = inputGate(x0)
    x1 = inputGate(x1)
    x2 = inputGate(x2)
    y0 = inputGate(y0)
    y1 = inputGate(y1)
    y2 = inputGate(y2)
    
    
    x0y0 = andGate(x0, y0)
    x0y1 = andGate(x0, y1)
    x0y2 = andGate(x0, y2)
    x1y0 = andGate(x1, y0)
    x1y1 = andGate(x1, y1)
    x1y2 = andGate(x1, y2)
    x2y0 = andGate(x2, y0)
    x2y1 = andGate(x2, y1)
    x2y2 = andGate(x2, y2)
    
    
    t0 = xorGate(x1y1, x1y2)
    z0 = xorGate(t0, x2y1)
    t1 = xorGate(x2y2, x0y2)
    z1 = xorGate(t1, x2y0)
    t2 = xorGate(x0y0, x0y1)
    z2 = xorGate(t2, x1y0)
    
     
    if checkFunctionality:
        res, v0, v1 = compareExpsWithExev(z0.getSymbExp() ^ z1.getSymbExp() ^ z2.getSymbExp(), x & y)
        if res == None:
            print('# functionality (exhaustive evaluation): [OK]')
        else:
            print('# functionality (exhaustive evaluation): [KO]')
            print(res)
    
    if dumpCirc:
        dumpCircuit(circuitFilename, z0, z1, z2)
    
    nbLeak, nbCheck = checkSecurity(order, withGlitches, prop, z0, z1, z2)
    return nbLeak, nbCheck


if __name__ == '__main__':
    nbLeak, nbCheck = ti_and(*sys.argv[1:])
    print('# Total Nb. of expressions analysed: %d' % nbCheck)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)



