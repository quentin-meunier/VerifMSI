# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from .config import *
from .utils import *
from .node import *
from .simplify import *



def getReplacedGraph(node, selMask, childToReplace):
    def getReplacedGraphRec(node, selMask, childToReplace, m):
        if not isinstance(node, OpNode):
            return node
        children = []
        for child in node.children:
            if child in m:
                children.append(m[child])
                continue
            if child is selMask:
                children.append(childToReplace)
                continue
            if child is childToReplace:
                children.append(selMask)
                continue
            #if selMask in child.maskVarOcc:
            if selMask in child.maskingMaskOcc or selMask in child.otherMaskOcc:
                newChild = getReplacedGraphRec(child, selMask, childToReplace, m)
                children.append(newChild)
            else:
                children.append(child)
        n = OpNode(node.op, children)
        m[node] = n
        return n

    return getReplacedGraphRec(node, selMask, childToReplace, {})



def tps(nodeIn, verbose = False):
    if len(nodeIn.shareOcc) != 0:
        print('*** Error: Threshold Probing verification should not use a share representation but explicit secret variables and masks')
        sys.exit(1)
    return checkProperty(nodeIn, 'tps', None, verbose)


def ni(nodeIn, maxShareOcc, verbose = False):
    if len(nodeIn.secretVarOcc) != 0:
        print('*** Error: NI verification should use a share representation and not explicit secret variables')
        sys.exit(1)
    return checkProperty(nodeIn, 'ni', maxShareOcc, verbose)


def rni(nodeIn, diff, verbose = False):
    if len(nodeIn.secretVarOcc) != 0:
        print('*** Error: RNI verification should use a share representation and not explicit secret variables')
        sys.exit(1)
    return checkProperty(nodeIn, 'rni', diff, verbose)


def pini(nodeIn, params, verbose = False):
    if len(nodeIn.secretVarOcc) != 0:
        print('*** Error: PINI verification should use a share representation and not explicit secret variables')
        sys.exit(1)
    return checkProperty(nodeIn, 'pini', params, verbose)


def checkProperty(nodeIn, secProp, params, verbose):
    if verbose:
        print('# Call func tps on exp %s' % nodeIn)

    if secProp == 'ni':
        maxShareOcc = params
    elif secProp == 'rni':
        diff = params # Difference between the order of verification and the n-uplet size
    elif secProp == 'pini':
        maxSharesIndicesNum = params[0]
        outputSharesIndices = params[1]

    node = simplify(nodeIn)

    masksTaken = set()
    cpt = 0
    while True:
        if verbose:
            print('# Starting iteration %d' % cpt)
            print('# e = %s' % node)
        cpt += 1

        if secProp == 'tps':
            if len(node.secretVarOcc) == 0:
                if verbose:
                    print('# No more secret')
                return True
        elif secProp == 'ni':
            isNI = True
            for s in node.shareOcc:
                #print('len(node.shareOcc[s]) : %d - maxShareOcc : %d' % (len(node.shareOcc[s]), maxShareOcc));
                if len(node.shareOcc[s]) > maxShareOcc:
                    isNI = False
                    break
            if isNI:
                return True
        elif secProp == 'rni':
            isRNI = True
            for s in node.shareOcc:
                for anyOcc in node.shareOcc[s]:
                    nbShares = anyOcc.nbShares
                    break
                if len(node.shareOcc[s]) >= nbShares - diff:
                    isRNI = False
                    break
            if isRNI:
                return True
        elif secProp == 'pini':
            #print('# outputSharesIndices: %s' % ' '.join(map(lambda x: '%d' % x, outputSharesIndices)))
            internalSharesIndices = set()
            for s in node.shareOcc:
                for sh in node.shareOcc[s]:
                    num = sh.shareNum
                    if num not in outputSharesIndices:
                        internalSharesIndices.add(num)
            if len(internalSharesIndices) <= maxSharesIndicesNum:
                return True


        if len(node.currentlyMasking) != 0:
            if verbose:
                print('# Masking mask, return True')
            return True
 
        # Choice of CTR:
        # - Choose mask m which minimizes the number of nodes with occurrence of m (CTR Bases + other Occ)
        # - For this m, choose CTR Base with the highest count
        # - For this CTR Base, choose the CTR with the max height for the same count
        maskingMaskOcc = node.maskingMaskOcc
        otherMaskOcc = node.otherMaskOcc
        minOtherOcc = 1000000
        minMaskingOcc = 1000000
        minRootMask = False
        selMask = None
        for m in maskingMaskOcc:
            nbMaskingOcc = len(maskingMaskOcc[m])

            try:
                nbOtherOcc = len(otherMaskOcc[m])
            except:
                nbOtherOcc = 0

            # FIXME: change the condition nbMaskingOcc == 1 with the fact that the number of maskingOcc has strictly decreased since the last time the mask was taken?
            if m in masksTaken and not (nbMaskingOcc == 1 and nbOtherOcc == 0):
                continue
            
            rootMask = (node.op == 'C' and m in node.children)

            # Heuristic:
            # 1. First, minimize the number of otherOcc
            # 2. For the masks with a min number of otherOcc, minimize the number of maskingOcc
            # (Old heuristic: minimize total number of occurrences)
            if (not rootMask and minRootMask) or (rootMask == minRootMask and (nbOtherOcc < minOtherOcc or (nbOtherOcc == minOtherOcc and nbMaskingOcc < minMaskingOcc))):
                selMask = m
                minRootMask = rootMask
                minOtherOcc = nbOtherOcc
                minMaskingOcc = nbMaskingOcc

        if selMask == None:
            if verbose:
                print('# No mask can be taken')
            return False

        if verbose:
            print('# Choosing mask %s (number of parent nodes: %d)' % (selMask, (minMaskingOcc + minOtherOcc)))

        maxCount = 0
        selCtrBase = None
        occs = maskingMaskOcc[selMask]
        for ctrBase in occs:
            if occs[ctrBase][ctrBase][0] > maxCount:
                maxCount = occs[ctrBase][ctrBase][0]
                selCtrBase = ctrBase

        if verbose:
            print('# Choosing following ctr base with %d occurrences: %s' % (maxCount, selCtrBase))

        maxHeight = -1
        selCtr = None
        for ctr in occs[selCtrBase]:
            height = occs[selCtrBase][ctr][1]
            if occs[selCtrBase][ctr][0] == maxCount and height > maxHeight:
                maxHeight = height
                selCtr = ctr
        
        if verbose:
            print('# Choosing following ctr with a height of %d: %s' % (maxHeight, selCtr))

        # FIXME: currently the results is not deterministic, and a some verifications can either
        #        succeed or fail, even if it is a very rare case
        #        There are three non deterministic choices, and in order to make them deterministic,
        #        we can for example take the min or max of the node number
        #        I still expect this to slow down the execution time a little...

        masksTaken.add(selMask)
        node = getReplacedGraph(node, selMask, selCtr)

        if verbose:
            print('# Replacing %s with %s' % (selCtr, selMask))
            print('# and other occurrences of %s with %s' % (selMask, selCtr))

        # Simplify
        node = simplify(node)


