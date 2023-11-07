# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from .utils import *
from .node import *


allRules = {}



def addSimpRule(s, t):
    #print('# Adding rule: %s -> %s' % (s, t))
    allRules[s.hh] = (s, t)


def getEquiv(e):
    for r in allRules:
        if e.hh == r:
            #print('# Found rule %s -> %s' % (allRules[r][0], allRules[r][1]))
            return copyExp(e, allRules[r][0], allRules[r][1])
    return None




def getMapping(exp, orig):

    #print('# SymbInExp : [' + ', '.join(map(lambda x: '%s' % x, symbInExp)) + ']')
    #print('# SymbInOrig: [' + ', '.join(map(lambda x: '%s' % x, symbInOrig)) + ']')
    # Enumerates all possible permutations
    m = {}
    #mappingsDone = []
    origRoot = orig

    def enumMappingsRec(exps, origs, childNums, taken, nbRemainingChildren):
        # exps: list of nodes in exp from bottom (current node) to root
        # origs: list of nodes in orig from bottom (current node) to root
        # childNums: list of current childNum indexes for the i-th parent node in orig
        # taken: list of 'taken' array for the i-th parent node in exp
        
        #print('# enumMappingRec : orig = %s -- exp = %s' % (origs[0], exps[0]))

        nonlocal m
        
        exp = exps[0]
        orig = origs[0]
        childrenTaken = taken[0]
        
        if nbRemainingChildren[0] == 0:

            idx = 1
            while idx < len(origs) and (childNums[idx] == len(origs[idx].children) or not origs[idx].children[childNums[idx]] is orig):
                idx += 1

            if idx == len(origs):
                # Return mapping
                #print('# Return mapping: ', end = '')
                #for k in m:
                #    print('%s -> %s, ' % (k, m[k]), end = '')
                return True

            exps.insert(0, exps[idx])
            origs.insert(0, origs[idx])
            if nbRemainingChildren[idx] > 0:
                childNums.insert(0, childNums[idx] + 1)
                nbRemainingChildren.insert(0, nbRemainingChildren[idx] - 1)
            else:
                assert(nbRemainingChildren[idx] == 0)
                childNums.insert(0, childNums[idx])
                nbRemainingChildren.insert(0, 0)
            taken.insert(0, taken[idx].copy())

            res = enumMappingsRec(exps, origs, childNums, taken, nbRemainingChildren)
            if res:
                return True

            exps.pop(0)
            origs.pop(0)
            childNums.pop(0)
            taken.pop(0)
            nbRemainingChildren.pop(0)

            return False


        childNum = childNums[0]
        child = orig.children[childNum]
        for i in range(nbRemainingChildren[0]):
            # Taking i-th non taken symbol
            j = 0
            k = 0
            while childrenTaken[k]:
                k += 1

            while j != i:
                j += 1
                k += 1
                while childrenTaken[k]:
                    k += 1

            if child.hh == exp.children[k].hh:
                if isinstance(child, SymbNode):
                    if child not in m:
                        m[child] = exp.children[k]
                        #print('#       m[%s] <- %s' % (child, m[child]))
                        #print('#       (' + ', '.join(map(lambda x: 'm[%s] = %s' % (x, m[x]), m.keys())) + ')')
                        #continueLater = False
                        #for mappingDone in mappingsDone:
                        #    if mappingDone == m:
                        #        continueLater = True
                        #        print('# Mapping Done, breaking')
                        #        break
                        #if continueLater:
                        #    del m[child]
                        #    print('#       m[%s] unset' % child)
                        #    continue
                        #mappingsDone.append(m.copy())
                        childrenTaken[k] = True

                        childNums[0] += 1
                        nbRemainingChildren[0] -= 1
                        res = enumMappingsRec(exps, origs, childNums, taken, nbRemainingChildren)
                        if res:
                            return True

                        nbRemainingChildren[0] += 1
                        childNums[0] -= 1

                        childrenTaken[k] = False
                        del m[child]
                        #print('#       m[%s] unset' % child)
                    elif m[child] is exp.children[k]:
                        childrenTaken[k] = True

                        childNums[0] += 1
                        nbRemainingChildren[0] -= 1
                        res = enumMappingsRec(exps, origs, childNums, taken, nbRemainingChildren)
                        if res:
                            return True
                        nbRemainingChildren[0] += 1
                        childNums[0] -= 1

                        childrenTaken[k] = False
                elif isinstance(child, OpNode):
                    childrenTaken[k] = True

                    origs.insert(0, child)
                    exps.insert(0, exp.children[k])
                    childNums.insert(0, 0)
                    taken.insert(0, [False] * len(child.children))
                    nbRemainingChildren.insert(0, len(child.children))

                    res = enumMappingsRec(exps, origs, childNums, taken, nbRemainingChildren)
                    if res:
                        return True

                    origs.pop(0)
                    exps.pop(0)
                    childNums.pop(0)
                    taken.pop(0)
                    nbRemainingChildren.pop(0)

                    childrenTaken[k] = False

        return False

    nbChildren = len(exp.children)
    taken = [[False] * nbChildren]
    res = enumMappingsRec([exp], [orig], [0], taken, [nbChildren])
    if res:
        return m
    else:
        return None






def copyExp(e, orig, target):

    mapping = getMapping(e, orig)
    if mapping == None:
        return None

    #print('# Final Mapping')
    #for var in mapping:
    #    print('# %s -> %s' % (var, mapping[var]))

    def copyExpRec(trg):
        if isinstance(trg, SymbNode):
            return mapping[trg]
        if isinstance(trg, ConstNode):
            return trg
        if isinstance(trg, StrNode):
            return trg
        # OpNode
        children = []
        for c in trg.children:
            newChild = copyExpRec(c)
            children.append(newChild)
        n = OpNode(trg.op, children)
        return n

    retval = copyExpRec(target)
    #print('# Replacing %s with %s' % (e, retval))
    return retval


