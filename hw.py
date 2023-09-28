# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from .node import *
from .simplify import *
from .check_leakage import *


class HWElement(object):
    
    nodeNum = 0
    nbNIcalls = 0
    remSingleInputProbesOpt = True
    remRedundantProbesOpt = True
    bartheOpt = False

    def __init__(self):
        self.num = HWElement.nodeNum
        HWElement.nodeNum += 1


    @staticmethod
    def dumpCircuitGates(filename, hwElems):
        f = open(filename, 'w')
        content = 'digraph g {\n'
        content += '    rankdir="LR";'
        for hwe in hwElems:
            if isinstance(hwe, Gate):
                if hwe.op == '|':
                    s = 'OR Gate (%d)\n/%d/' % (hwe.num, hwe.symbExp.width)
                elif hwe.op == '&':
                    s = 'AND Gate (%d)\n/%d/' % (hwe.num, hwe.symbExp.width)
                elif hwe.op == '^':
                    s = 'XOR Gate (%d)\n/%d/' % (hwe.num, hwe.symbExp.width)
                elif hwe.op == 'I':
                    n = hwe.symbExp
                    if isinstance(n, SymbNode):
                        s = 'Symbol: %s [%s] (%d)\n/%d/' % (n.symb, n.symbType, hwe.num, n.width)
                    elif isinstance(n, ConstNode):
                        s = 'Const: %d (%d)\n/%d/' % (n.cst, hwe.num, n.width)
                    else:
                        s = 'Exp: %s (%d)\n/%d/' % (n, hwe.num, n.width)
                else:
                    assert(False)
            elif isinstance(hwe, Register):
                s = 'Register (%d)\n/%d/' % (hwe.num, hwe.symbExp.width)
            else:
                assert(False)
            
            shape = isinstance(hwe, Register) and 'rectangle' or 'oval'
            content += '   N%d [shape=%s, label=\"%s\"];\n' % (hwe.num, shape, s)
            for a in hwe.inputs:
                content += '   edge[tailclip=true];\n'
                content += '   N%d -> N%d\n' % (a.num, hwe.num)

        content += '}'
        f.write(content)
        f.close()



class Gate(HWElement):

    def __init__(self, op, *inputs):
        if op == 'I':
            if not isinstance(inputs[0], Node):
                print('*** Error: Input Gate only takes as parameter a symbolic variable or expression' % op)
                sys.exit(1)
        else:
            for inp in inputs:
                if isinstance(inp, Node):
                    print('*** Error: Gate \'%s\' cannot have a symbolic expression as input (expression is \'%s\')' % (op, inp))
                    sys.exit(1)
        HWElement.__init__(self)
        self.op = op
        if op == 'I':
            self.inputs = list()
            self.symbExp = inputs[0]
            self.leakageOut = set()
            self.leakageOut.add(inputs[0])
        else:
            self.inputs = inputs
            self.symbExp = simplify(Node.makeBitwiseNode(op, list(map(lambda x: x.symbExp, inputs))))
            self.leakageOut = set()
            for i in range(len(inputs)):
                self.leakageOut.update(inputs[i].leakageOut)


    def getSymbExp(self):
        return self.symbExp


    def __str__(self):
        s = ''
        s += 'Gate %s (%d)\n' % (self.op, self.num)
        s += '   Symbolic Exp: %s\n' % self.symbExp
        s += '   Leakage out: %s\n' % ', '.join(map(lambda x: '%s' % x, self.leakageOut))
        s += '   Inputs: ' + ', '.join(map(lambda x: 'Gate %d' % x.num, self.inputs)) + '\n'
        return s



def andGate(*children):
    return Gate('&', *children)


def orGate(*children):
    return Gate('|', *children)


def xorGate(*children):
    return Gate('^', *children)


def inputGate(child):
    return Gate('I', child)


class Register(HWElement):
    def __init__(self, inp):
        HWElement.__init__(self)
        self.inputs = [inp]
        self.symbExp = inp.symbExp
        self.leakageOut = set()
        self.leakageOut.add(inp.symbExp)

    def dump(filename):
        dumpCircuit(self, filename)

    def __str__(self):
        s = ''
        s += 'Register (%d)\n' % self.num
        s += '   Symbolic Exp: %s\n' % self.symbExp
        s += '   Leakage out:  %s\n' % ', '.join(map(lambda x: '%s' % x, self.leakageOut))
        s += '   Input:        Gate/Reg %d\n' % self.inputs[0].num
        return s


def getReachableGates(g, rg):
    if g not in rg:
        rg.add(g)
    for child in g.inputs:
        getReachableGates(child, rg)


def dumpCircuit(filename, *outputs):
    reachableGates = set()
    for gate in outputs:
        getReachableGates(gate, reachableGates)
    HWElement.dumpCircuitGates(filename, reachableGates)


def checkSecurity(order, withGlitches, secProp, *outputList):
    print('# Checking Security at order %d (%s, %s property)' % (order, withGlitches and 'with glitches' or 'no glitches', secProp))

    def tupleEnum(gateList, order, includePartialTuples):
        tuples = set()
        tupleLen = order
        t = [None] * order

        def tupleEnumRec(i, nbTaken, includePartialTuples):
            def getLeakExps(gates):
                t = set()
                for gate in gates:
                    if withGlitches:
                        for leakExp in gate.leakageOut:
                            t.add(leakExp)
                    else:
                        t.add(gate.symbExp)
                return t
 
            if nbTaken == tupleLen:
                tuples.add((tuple(getLeakExps(t)), tuple(t)))
                return

            if includePartialTuples and nbTaken > 0:
                tuples.add((tuple(getLeakExps(t[0:nbTaken])), tuple(t[0:nbTaken])))

            for idx in range(i, len(gateList)):
                t[nbTaken] = gateList[idx]
                tupleEnumRec(idx + 1, nbTaken + 1, includePartialTuples)

        tupleEnumRec(0, 0, includePartialTuples)
        return tuples


    #################
    def tupleEnumPINI(outputList, internalGatesList, order, includePartialTuples):

        tuples = set()

        def tupleEnumPINIOutputIndices(nbOutputIndices):
            nbShares = len(outputList[0])
            outputSharesTaken = [None] * nbOutputIndices

            def tupleEnumPINIOutputIndicesRec(nbOutputIndices, i, nbTaken):
                if nbTaken == nbOutputIndices:
                    tupleEnumPINIInternal(outputSharesTaken, order - nbOutputIndices)
                    return

                for idx in range(i, nbShares):
                    outputSharesTaken[nbTaken] = idx
                    tupleEnumPINIOutputIndicesRec(nbOutputIndices, idx + 1, nbTaken + 1)

            tupleEnumPINIOutputIndicesRec(nbOutputIndices, 0, 0)


        def tupleEnumPINIInternal(outputSharesTaken, nbInternal):
            
            sharesTakenTuple = tuple(outputSharesTaken)
            t = [None] * nbInternal
            outputSharesList = list()
            #print('# Output shares taken: ' + ' '.join(map(lambda x: '%d' % x, outputSharesTaken)))
            for i in outputSharesTaken:
                for output in outputList:
                    outputSharesList.append(output[i])
            
            def tupleEnumPINIInternalRec(i, nbTaken):
                def getLeakExps(gates):
                    t = set()
                    for gate in gates:
                        if withGlitches:
                            for leakExp in gate.leakageOut:
                                t.add(leakExp)
                        else:
                            t.add(gate.symbExp)
                    return t
 
                if nbTaken == nbInternal:
                    probeList = outputSharesList + t
                    #print('# Adding full tuple (' + ', '.join(map(lambda x: '%d' % x.num, sorted(probeList, key = lambda x: x.num))) + ')')
                    assert(nbTaken == order - len(sharesTakenTuple))
                    tuples.add((tuple(getLeakExps(probeList)), tuple(probeList), nbTaken, sharesTakenTuple))
                    return

                if includePartialTuples and nbTaken > 0:
                    probeList = outputSharesList + t[0:nbTaken]
                    #print('# Adding partial tuple (' + ', '.join(map(lambda x: '%d' % x.num, sorted(probeList, key = lambda x: x.num))) + ')')
                    tuples.add((tuple(getLeakExps(probeList)), tuple(probeList), nbTaken, sharesTakenTuple))

                for idx in range(i, len(internalGatesList)):
                    t[nbTaken] = internalGatesList[idx]
                    tupleEnumPINIInternalRec(idx + 1, nbTaken + 1)

            tupleEnumPINIInternalRec(0, 0)



        for nbOutputIndices in range(0, order + 1):
            tupleEnumPINIOutputIndices(nbOutputIndices)
        
        return tuples
    #################


    outputs = list()
    if isinstance(outputList[0], HWElement):
        outputList = [outputList]

    for elem in outputList:
        assert(isinstance(elem, list) or isinstance(elem, tuple))
        for gate in elem:
            assert(isinstance(gate, HWElement))
            outputs.append(gate)

    reachableGates = set()
    for gate in outputs:
        getReachableGates(gate, reachableGates)

    print('# Reachable gates (%d): ' % (len(reachableGates)) + ' '.join(map(lambda x: '%s' % x.num, reachableGates)))

    if withGlitches:
        doRemSingleInputProbesOpt = False
        # Removing components with redudant exps
        if False:
            reducedGates = reachableGates
        else:
            reducedGates = set()
            for gate in reachableGates:
                isSubset = False
                toRemove = set()
                for g in reducedGates:
                    if g.leakageOut.issubset(gate.leakageOut):
                        toRemove.add(g)
                    elif gate.leakageOut.issubset(g.leakageOut):
                        isSubset = True
                        break
                if not isSubset:
                    reducedGates.add(gate)
                for g in toRemove:
                    reducedGates.remove(g)
    elif secProp == 'ni' or secProp == 'rni' or secProp == 'sni' or secProp == 'pini':
        # Tuple reduction is not applicable to TPS
        # Checking if all input shares are part of the reachable gates
        reachableInputShares = set(filter(lambda x: isinstance(x, Gate) and x.op == 'I' and isinstance(x.symbExp, SymbNode) and x.symbExp.symbType == 'A', reachableGates))
        #print(' '.join(map(lambda x: '%s' % x.symbExp.symb, reachableInputShares)))
        reachableInputSharesSecrets = set(map(lambda x: (x.symbExp.origSecret, x.symbExp.nbShares), reachableInputShares))
        #print(' '.join(map(lambda x: '%s' % x[0].symb, reachableInputSharesSecrets)))
        allInputShares = True
        for t in reachableInputSharesSecrets:
            if len(list(filter(lambda x: x.symbExp.origSecret is t[0], reachableInputShares))) != t[1]:
                allInputShares = False
                break

        reducedGates = set(reachableGates)
        withdrawnGates = set()


        # Remove the gate / probe if it contains at most one share per input and no random
        doRemSingleInputProbesOpt = HWElement.remSingleInputProbesOpt and allInputShares
        if doRemSingleInputProbesOpt:
            if secProp == 'pini':
                print('# Removing single input probes')

                for g in sorted(reachableGates, key = lambda x: x.num):
                    verifyGate = True
                    moreThanOneOcc = False
                    if len(g.symbExp.shareOcc) == 1:
                        for secret in g.symbExp.shareOcc: # single secret, single iteration
                            if len(g.symbExp.shareOcc[secret]) == 1 and len(g.symbExp.maskingMaskOcc.keys()) + len(g.symbExp.otherMaskOcc.keys()) == 0:
                                print('# Removing gate %d: %s' % (g.num, g.symbExp))
                                reducedGates.remove(g)
                                withdrawnGates.add(g)
            else:
                print('# Removing Probes with at most 1 share / input and no random')

                for g in sorted(reachableGates, key = lambda x: x.num):
                    verifyGate = True
                    moreThanOneOcc = False
                    for secret in g.symbExp.shareOcc:
                        if len(g.symbExp.shareOcc[secret]) > 1:
                            moreThanOneOcc = True
                            break
                    if not moreThanOneOcc:
                        if len(g.symbExp.maskingMaskOcc.keys()) + len(g.symbExp.otherMaskOcc.keys()) == 0:
                            verifyGate = False
    
                    if not verifyGate:
                        print('# Removing gate %d: %s' % (g.num, g.symbExp))
                        reducedGates.remove(g)
                        withdrawnGates.add(g)
            

        # Remove the gate / probe if it has exactly the same masking randoms and the same or a subset of the input shares of another gate
        doRemRedundantProbesOpt = HWElement.remRedundantProbesOpt
        if doRemRedundantProbesOpt:
            print('# Removing Redundant Probes')

            for g in sorted(reducedGates, key = lambda x: x.num):
                verifyGate = True
                if isinstance(g.symbExp, SymbNode) and g.symbExp.symbType == 'M' or len(g.symbExp.otherMaskOcc) == 0:
                    for h in reachableGates:
                        if g == h:
                            continue
                        if h in withdrawnGates:
                            continue
                        gShares = set()
                        for secret in g.symbExp.shareOcc:
                            for sh in g.symbExp.shareOcc[secret]:
                                gShares.add(sh)
                        hShares = set()
                        for secret in h.symbExp.shareOcc:
                            for sh in h.symbExp.shareOcc[secret]:
                                hShares.add(sh)

                        # FIXME? For SNI and PINI, shouldn't we prevent the case in which the larger gate is an internal gate and the redundant gate an output gate?
                        if len(h.symbExp.otherMaskOcc) == 0 and set(g.symbExp.maskingMaskOcc.keys()) == set(h.symbExp.maskingMaskOcc.keys()) and gShares.issubset(hShares):
                            #print('# Shares of g: %s' % ', '.join(map(lambda x: '%s' % x, gShares)))
                            #print('# Shares of h: %s' % ', '.join(map(lambda x: '%s' % x, hShares)))
                            #print('# Larger Gate: %d: %s' % (h.num, h.symbExp))
                            verifyGate = False
                            break
                        elif isinstance(g.symbExp, SymbNode) and g.symbExp.symbType == 'M' and len(h.symbExp.otherMaskOcc) == 0 and set([g.symbExp]) == set(h.symbExp.maskingMaskOcc.keys()):
                            verifyGate = False
                            #print('# Larger Gate for %s: %d: %s' % (g.symbExp, h.num, h.symbExp))
                            break

                if not verifyGate:
                    print('# Removing gate %d: %s' % (g.num, g.symbExp))
                    # sorted() returns a copy of the list, so it is safe to modify reducedGates
                    reducedGates.remove(g)
                    withdrawnGates.add(g)

    else:
        assert(secProp == 'tps')
        reducedGates = reachableGates
        doRemSingleInputProbesOpt = False


    gates = list(reducedGates)
    print('# Reduced gates (%d):   ' % (len(reducedGates)) + ' '.join(map(lambda x: '%s' % x.num, gates)))
    print('\n'.join(map(lambda x: '# Gate %d: %s' % (x.num, x.symbExp), sorted(gates, key = lambda x: x.num))))

    if (secProp == 'ni' or secProp == 'tps') and HWElement.bartheOpt:

        expNames = {}
        expNum = 0
        reducedGatesExp = set()
        for g in reducedGates:
            if withGlitches:
                for leakExp in g.leakageOut:
                    reducedGatesExp.add(leakExp)
            else:
                reducedGatesExp.add(g.symbExp)
                expNames[g.symbExp] = 'e%d' % expNum
                expNum += 1
 
        def checkProp(e, order):
            if secProp == 'tps':
                return checkTpsVal(e)
            else:
                return checkNIVal(e, order)


        def choose(e, nb):
            s = set()
            cnt = 0
            for elem in e:
                s.add(elem)
                cnt += 1
                if cnt == nb:
                    break
            return s

        def extend(y, e):
            if len(e) == 0:
                return y
            
            elem = choose(e, 1)
            res = checkProp(Concat(*tuple(y | elem)), order)
            HWElement.nbNIcalls += 1
            elemSet = set(elem)
            if res[0]:
                return extend(y | elemSet, e - elemSet)
            else:
                return extend(y, e - elemSet)

        def tupleEnumBis(expsSet, order):
            # same idea as tupleEnum but with the following differences:
            # - it does not enumerates on gates, but directly on symb exps
            # - there is no partial tuples
            tuples = set()
            expsList = tuple(expsSet)
            t = [None] * order

            def tupleEnumBisRec(i, nbTaken):
                if nbTaken == order:
                    tuples.add(frozenset(t))
                    return

                for idx in range(i, len(expsList)):
                    t[nbTaken] = expsList[idx]
                    tupleEnumBisRec(idx + 1, nbTaken + 1)

            tupleEnumBisRec(0, 0)
            return tuples

        def check(x, d, e, depth):
            def localPrint(param):
                print('# ' + '   ' * depth, end = '')
                print('%s' % param)

            #localPrint('check d = %d' % d)
            #localPrint('x = [' + ', '.join(map(lambda u: '%s' % expNames[u], x)) + ']')
            #localPrint('  = [' + ', '.join(map(lambda u: '%s' % u, x)) + ']')
            #localPrint('e = [' + ', '.join(map(lambda u: '%s' % expNames[u], e)) + ']')
            #localPrint('  = [' + ', '.join(map(lambda u: '%s' % u, e)) + ']')
            assert(len(x) + d == order)
            if d <= len(e):
                y = choose(e, d)
                #localPrint('y = [' + ', '.join(map(lambda u: '%s' % expNames[u], y)) + ']')
                #localPrint('  = [' + ', '.join(map(lambda u: '%s' % u, y)) + ']')
                #localPrint('checkNIVal(' + ', '.join(map(lambda u: '%s' % expNames[u], tuple(x | y))) + ')')
                #localPrint('checkNIVal(' + ', '.join(map(lambda u: '%s' % u, tuple(x | y))) + ')')
                z = x | y
                h = checkProp(Concat(*tuple(z)), order)
                HWElement.nbNIcalls += 1
                if not h[0]:
                    #localPrint('return False')
                    return False
                yc = extend(z, e - y)
                #localPrint('yc = [' + ', '.join(map(lambda u: '%s' % expNames[u], yc)) + ']')
                #localPrint('   = [' + ', '.join(map(lambda u: '%s' % u, yc)) + ']')
                eMinusyc = e - yc
                ycMinusx = yc - x
                res = check(x, d, eMinusyc, depth + 1)
                if not res:
                    #localPrint('not res, return False')
                    return False
                for i in range(1, d):
                    tuples = tupleEnumBis(ycMinusx, i)
                    for t in tuples:
                        res = check(x | t, d - i, eMinusyc, depth + 1)
                        if not res:
                            return False
                return True
            else:
                return True

        print('# reducedGatesExp:')
        print('\n'.join(map(lambda x: '#    Exp: %s' % x, reducedGatesExp)))

        res = check(set(), order, reducedGatesExp, 0)
        print('# Res for Barthe Algo: %s' % str(res))
        print('# Nb. NI calls: %d' % HWElement.nbNIcalls)
        if res:
            return 0, HWElement.nbNIcalls
        else:
            return 1, HWElement.nbNIcalls
    else:

        print('# Starting tuple enumeration')
        if secProp == 'pini':
            internalGates = list(set(gates) - set(outputs))
            #print('# Internal gates: ' + ', '.join(map(lambda x: '%d' % x.num, sorted(internalGates, key = lambda x: x.num))))
            tuples = tupleEnumPINI(outputList, internalGates, order, doRemSingleInputProbesOpt)
        else:
            tuples = tupleEnum(gates, order, doRemSingleInputProbesOpt)
        print('# Number of tuples: %d' % len(tuples))
        #for t in tuples:
        #    print('# (' + ', '.join(map(lambda x: '%d' % x.num, sorted(t[1], key = lambda x: x.num))) + ')')

        leakingHwe = list()
        for t in tuples:
            #print('# Checking expression for component(s) (%s): %s' % (', '.join(map(lambda x: '%d' % x.num, t[1])), ', '.join(map(lambda x: '%s' % x, t[0]))))
            if secProp == 'tps':
                res = checkTpsVal(Concat(*t[0]))
            elif secProp == 'ni':
                #print('# checking NI for exps %s and maxShareOcc = %d' % (', '.join(map(lambda x: '%s' % x, t[0])), len(t[1])))
                res = checkNIVal(Concat(*t[0]), len(t[1]))
            elif secProp == 'rni':
                #print('# checking RNI for exps %s and maxShareOcc = (nbShares - 1) - %d' % (', '.join(map(lambda x: '%s' % x, t[0])), (order - len(t[1]))))
                res = checkRNIVal(Concat(*t[0]), (order - len(t[1])))
            elif secProp == 'sni':
                nbOutputProbes = 0
                for probe in t[1]:
                    if probe in outputs:
                        nbOutputProbes += 1
                res = checkNIVal(Concat(*t[0]), len(t[1]) - nbOutputProbes)
            elif secProp == 'pini':
                res = checkPINIVal(Concat(*t[0]), (t[2], t[3]))
            else:
                assert(False)

            if not res[0]:
                #print('# Leaking expression for component(s) (%s): %s' % (', '.join(map(lambda x: '%d' % x.num, t[1])), ', '.join(map(lambda x: '%s' % x, t[0]))))
                leakingHwe.append(t)


        if len(leakingHwe) != 0:
            print('# Following Components\' outputs are not %s secure at order %d %s glitches:' % (secProp, order, withGlitches and 'with' or 'without'))
            for hwe in leakingHwe:
                print('# Leaking expression for component(s) (%s): %s' % (', '.join(map(lambda x: '%d' % x.num, hwe[1])), ', '.join(map(lambda x: '%s' % x, hwe[0]))))
        else:
            print('# Circuit is secure in the %s security model at order %d %s glitches' % (secProp, order, withGlitches and 'with' or 'without'))

    return len(leakingHwe), len(tuples)

