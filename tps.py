#!/usr/bin/python

# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the Muse project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function

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


def rni(nodeIn, maxShareOcc, verbose = False):
    if len(nodeIn.secretVarOcc) != 0:
        print('*** Error: RNI verification should use a share representation and not explicit secret variables')
        sys.exit(1)
    return checkProperty(nodeIn, 'rni', maxShareOcc, verbose)


def pini(nodeIn, maxShareOcc, verbose = False):
    if len(nodeIn.secretVarOcc) != 0:
        print('*** Error: PINI verification should use a share representation and not explicit secret variables')
        sys.exit(1)
    return checkProperty(nodeIn, 'pini', maxShareOcc, verbose)


def checkProperty(nodeIn, secProp, maxShareOcc, verbose):
    if verbose:
        print('# Call func tps on exp %s' % nodeIn)

    node = simplify(nodeIn)

    masksTaken = set()
    cpt = 0
    while True:
        if verbose:
            print('# Starting iteration %d' % cpt)
            print('# e = %s' % node)
        #node.dump('dot/graph_%d.dot' % cpt)
        cpt += 1

        if secProp == 'tps':
            if len(node.secretVarOcc) == 0:
                if verbose:
                    print('# No more secret')
                return True
        elif secProp == 'ni':
            isNI = True
            for s in node.shareOcc:
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
                if len(node.shareOcc[s]) >= nbShares - maxShareOcc:
                    isRNI = False
                    break
            if isRNI:
                return True
        elif secProp == 'pini':
            maxShareOccReal = maxShareOcc[0]
            outputIndexes = maxShareOcc[1]
            isPINI = False
            for s in node.shareOcc:
                nbOcc = 0
                for sh in node.shareOcc[s]:
                    num = int(sh.name[-2]) # FIXME: fails if ten or more shares... add num in node??
                    if num not in outputIndexes:
                        nbOcc += 1
                if nbOcc > maxShareOccReal:
                    isPINI = False
                    break
            if isPINI:
                return True


        if len(node.currentlyMasking) != 0:
            return True
 
        # Choice of CTR:
        # - Choose mask m which minimizes the number of nodes with occurrence of m (CTR Bases + other Occ)
        # - For this m, choose CTR Base with the highest count
        # - For this CTR Base, choose the CTR with the max height for the same count
        maskingMaskOcc = node.maskingMaskOcc
        otherMaskOcc = node.otherMaskOcc
        minOcc = 1000000 # FIXME...
        selMask = None
        for m in maskingMaskOcc:
            # QM FIXME
            # Allow to take a masks several times, as long as its number of occs (masking? total? sum? masking AND other?) decreases
            # (save in m the number of occs when chosen)
            if m in masksTaken:
                continue

            if m in maskingMaskOcc:
                nbMaskingOp = len(maskingMaskOcc[m])
            else:
                assert(False)
                continue

            if m in otherMaskOcc:
                nbOtherOp = len(otherMaskOcc[m])
            else:
                nbOtherOp = 0

            # QM FIXME: try this heuristic
            # 1. First, minimize the number of otherOcc
            # 2. For the masks with a min number of otherOcc, minimize the number of maskingOcc
            nbOcc = nbMaskingOp + nbOtherOp
            if nbOcc < minOcc:
                minOcc = nbOcc
                selMask = m

        if selMask == None:
            if verbose:
                print('# No mask can be taken')
            return False

        if verbose:
            print('# Choosing mask %s (number of parent nodes: %d)' % (selMask, minOcc))

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

        # FIXME: do a deterministic choice? (for each of the three choices, add a comparison on node hash)

        masksTaken.add(selMask)
        node = getReplacedGraph(node, selMask, selCtr)

        if verbose:
            print('# Replacing %s with %s' % (selCtr, selMask))
            print('# and other occurrences of %s with %s' % (selMask, selCtr))

        #node.dump('dot/graph_%d_end.dot' % (cpt - 1))

        # Simplify
        node = simplify(node)


