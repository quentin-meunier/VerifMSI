# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

import sys

from .config import *
from .utils import *
from .node import *
from .simplify import *
from .concrev import secPropValidity, isTPSWithExev, isNIWithExev, isRNIWithExev, isPINIWithExev, isOPINIWithExev


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
            if selMask in child.maskingMaskOcc or selMask in child.otherMaskOcc:
                newChild = getReplacedGraphRec(child, selMask, childToReplace, m)
                children.append(newChild)
            else:
                children.append(child)
        n = OpNode(node.op, children)
        m[node] = n
        return n

    return getReplacedGraphRec(node, selMask, childToReplace, {})


def removeConstOperandsFromPlusRec(node, m):
    if not isinstance(node, OpNode) or not node.hasPlus:
        return node
    children = []
    for child in node.children:
        if child in m:
            children.append(m[child])
            continue
        if node.op == '+' and isinstance(child, ConstNode):
            continue
        newChild = removeConstOperandsFromPlusRec(child, m)
        children.append(newChild)
    if children == list(node.children):
        m[node] = node
        return node
    if len(children) == 0:
        assert False
        n = Const(0, node.width)
        m[node] = n
        return n
    if len(node.children) != len(children) and len(children) == 1:
        assert node.op == '+'
        n = children[0]
        m[node] = n
        return n
    n = OpNode(node.op, children)
    m[node] = n
    return n


def removeConstOperandsFromPlus(node):
    if not node.hasPlus:
        return node
    m = {}
    res = removeConstOperandsFromPlusRec(node, m)
    if res is not node:
        return simplify(res)
    return node


def checkPropertyWrapper(nodeIn, secProp, params, bitDecompose=False, noFalsePositive=False, verbose=False):
    if isinstance(nodeIn, (list, tuple, set)):
        nodes = [simplify(n, usbv=bitDecompose) for n in nodeIn]
        c = simplify(Concat(*nodes[::-1]) if len(nodes) > 1 else nodes[0])
    else:
        c = simplify(nodeIn, usbv=bitDecompose)
    return checkProperty(c, secProp, params, noFalsePositive, verbose)


def tps(nodeIn, bitDecompose=False, verbose=False):
    secPropValidity(nodeIn, TPS)
    return checkPropertyWrapper(nodeIn, TPS, None, bitDecompose, False, verbose)


def tpsNoFalsePositive(nodeIn, bitDecompose=False, verbose=False):
    secPropValidity(nodeIn, TPS)
    return checkPropertyWrapper(nodeIn, TPS, None, bitDecompose, True, verbose)


def ni(nodeIn, maxShareOcc, bitDecompose=False, verbose=False):
    secPropValidity(nodeIn, NI)
    return checkPropertyWrapper(nodeIn, NI, maxShareOcc, bitDecompose, False, verbose)


def niNoFalsePositive(nodeIn, maxShareOcc, bitDecompose=False, verbose=False):
    secPropValidity(nodeIn, NI)
    return checkPropertyWrapper(nodeIn, NI, maxShareOcc, bitDecompose, True, verbose)


def rni(nodeIn, diff, bitDecompose=False, verbose=False):
    secPropValidity(nodeIn, RNI)
    return checkPropertyWrapper(nodeIn, RNI, diff, bitDecompose, False, verbose)


def rniNoFalsePositive(nodeIn, diff, bitDecompose=False, verbose=False):
    secPropValidity(nodeIn, RNI)
    return checkPropertyWrapper(nodeIn, RNI, diff, bitDecompose, True, verbose)


def pini(nodeIn, maxShareOcc, outputIndexes=None, bitDecompose=False, verbose=False):
    if isinstance(maxShareOcc, tuple):
        outputIndexes = maxShareOcc[1]
        maxShareOcc = maxShareOcc[0]
    secPropValidity(nodeIn, PINI)
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    return checkPropertyWrapper(nodeIn, PINI, (maxShareOcc, outputIndexes), bitDecompose, False, verbose)


def piniNoFalsePositive(nodeIn, maxShareOcc, outputIndexes=None, bitDecompose=False, verbose=False):
    if isinstance(maxShareOcc, tuple):
        outputIndexes = maxShareOcc[1]
        maxShareOcc = maxShareOcc[0]
    secPropValidity(nodeIn, PINI)
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    return checkPropertyWrapper(nodeIn, PINI, (maxShareOcc, outputIndexes), bitDecompose, True, verbose)


def opini(nodeIn, maxShareOcc, outputIndexes=None, allOutputLeakages=None, bitDecompose=False, verbose=False):
    if isinstance(maxShareOcc, tuple):
        outputIndexes = maxShareOcc[1] if len(maxShareOcc) > 1 else None
        allOutputLeakages = maxShareOcc[2] if len(maxShareOcc) > 2 else None
        maxShareOcc = maxShareOcc[0]
    secPropValidity(nodeIn, OPINI)
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    else:
        outputIndexes = set(outputIndexes)
    if allOutputLeakages is None:
        allOutputLeakages = []

    additionalInputIndexes = set()
    probesLeakagesWithNewOutputs = [nodeIn] if not isinstance(nodeIn, (list, tuple)) else list(nodeIn)

    while True:
        res = checkPropertyWrapper(probesLeakagesWithNewOutputs, OPINI, (maxShareOcc, outputIndexes, additionalInputIndexes), bitDecompose, False, verbose)
        if not res:
            return False
        elif len(additionalInputIndexes) == 0:
            return True
        maxShareOcc = maxShareOcc - len(additionalInputIndexes)
        for idx in additionalInputIndexes:
            outputIndexes.add(idx)
            for output in allOutputLeakages:
                probesLeakagesWithNewOutputs.append(output[idx])
        additionalInputIndexes.clear()


def opiniNoFalsePositive(nodeIn, maxShareOcc, outputIndexes=None, allOutputLeakages=None, bitDecompose=False, verbose=False):
    if isinstance(maxShareOcc, tuple):
        outputIndexes = maxShareOcc[1] if len(maxShareOcc) > 1 else None
        allOutputLeakages = maxShareOcc[2] if len(maxShareOcc) > 2 else None
        maxShareOcc = maxShareOcc[0]
    secPropValidity(nodeIn, OPINI)
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    else:
        outputIndexes = set(outputIndexes)
    if allOutputLeakages is None:
        allOutputLeakages = []

    additionalInputIndexes = set()
    probesLeakagesWithNewOutputs = [nodeIn] if not isinstance(nodeIn, (list, tuple)) else list(nodeIn)

    while True:
        res = checkPropertyWrapper(probesLeakagesWithNewOutputs, OPINI, (maxShareOcc, outputIndexes, additionalInputIndexes), bitDecompose, True, verbose)
        if not res:
            return False
        elif len(additionalInputIndexes) == 0:
            return True
        maxShareOcc = maxShareOcc - len(additionalInputIndexes)
        for idx in additionalInputIndexes:
            outputIndexes.add(idx)
            for output in allOutputLeakages:
                probesLeakagesWithNewOutputs.append(output[idx])
        additionalInputIndexes.clear()


def checkProperty(nodeIn, secProp, params, noFalsePositive=False, verbose=False):
    if verbose:
        print('# Call func tps on exp %s' % nodeIn)

    if secProp == NI or secProp == 'ni':
        maxShareOcc = params
    elif secProp == RNI or secProp == 'rni':
        diff = params
    elif secProp == PINI or secProp == 'pini':
        maxShareOcc = params[0]
        outputIndexes = params[1]
    elif secProp == OPINI or secProp == 'opini':
        maxShareOcc = params[0]
        outputIndexes = params[1]
        additionalInputIndexes = params[2]

    node = nodeIn
    if verifRemoveCstInAddEnable():
        node = removeConstOperandsFromPlus(node)

    masksTaken = set()
    cpt = 0
    while True:
        if verbose:
            print('# Starting iteration %d' % cpt)
            print('# e = %s' % node)
        cpt += 1

        if secProp == TPS or secProp == 'tps':
            if len(node.secretVarOcc) == 0:
                if verbose:
                    print('# No more secret')
                return True
        elif secProp == NI or secProp == 'ni':
            isNI = True
            for s in node.shareOcc:
                if len(node.shareOcc[s]) > maxShareOcc:
                    isNI = False
                    break
            if isNI:
                return True
        elif secProp == RNI or secProp == 'rni':
            isRNI = True
            for s in node.shareOcc:
                nbTotalShares = s.nbShares if s.nbShares is not None else next(iter(node.shareOcc[s])).nbShares
                if len(node.shareOcc[s]) + diff >= nbTotalShares:
                    isRNI = False
                    break
            if isRNI:
                return True
        elif secProp == PINI or secProp == 'pini':
            internalSharesIndexes = set()
            for s in node.shareOcc:
                for sh in node.shareOcc[s]:
                    num = sh.shareNum
                    if num not in outputIndexes:
                        internalSharesIndexes.add(num)
            if len(internalSharesIndexes) <= maxShareOcc:
                return True

        if len(node.currentlyMasking) != 0:
            if verbose:
                print('# Masking mask, return True')
            return True

        # Choice of CTR:
        # - Choose mask m which minimizes the number of nodes with occurrence of m (CTR Bases + other Occ)
        # - For this m, choose CTR Base with the lowest count
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
            except Exception:
                nbOtherOcc = 0

            if m in masksTaken and not (nbMaskingOcc == 1 and nbOtherOcc == 0):
                continue

            rootMask = (node.op == 'C' and m in node.children)

            if (not rootMask and minRootMask) or (rootMask == minRootMask and (nbOtherOcc < minOtherOcc or (nbOtherOcc == minOtherOcc and nbMaskingOcc < minMaskingOcc))):
                selMask = m
                minRootMask = rootMask
                minOtherOcc = nbOtherOcc
                minMaskingOcc = nbMaskingOcc

        if selMask is None:
            if secProp == OPINI or secProp == 'opini':
                internalSharesIndexes = set()
                for s in node.shareOcc:
                    for sh in node.shareOcc[s]:
                        num = sh.shareNum
                        if num not in outputIndexes:
                            internalSharesIndexes.add(num)
                if len(internalSharesIndexes) > maxShareOcc:
                    if verbose:
                        print('# No mask can be taken')
                    if noFalsePositive:
                        if verbose:
                            print('# NoFalsePositive enabled, calling enumeration')
                        return isOPINIWithExev(node, maxShareOcc, outputIndexes, additionalInputIndexes)
                    else:
                        return False
                for num in internalSharesIndexes:
                    additionalInputIndexes.add(num)
                return True

            if verbose:
                print('# No mask can be taken')
            if noFalsePositive:
                if verbose:
                    print('# NoFalsePositive enabled, calling enumeration')
                if secProp == TPS or secProp == 'tps':
                    return isTPSWithExev(node)
                elif secProp == NI or secProp == 'ni':
                    return isNIWithExev(node, maxShareOcc)
                elif secProp == PINI or secProp == 'pini':
                    return isPINIWithExev(node, maxShareOcc, outputIndexes)
                elif secProp == RNI or secProp == 'rni':
                    return isRNIWithExev(node, diff)
            return False

        if verbose:
            print('# Choosing mask %s (number of parent nodes: %d)' % (selMask, (minMaskingOcc + minOtherOcc)))

        minCount = float('inf')
        selCtrBase = None
        occs = maskingMaskOcc[selMask]
        for ctrBase in occs:
            count = occs[ctrBase][ctrBase][0]
            if count < minCount:
                minCount = count
                selCtrBase = ctrBase
        if selCtrBase is None:
            for ctrBase in occs:
                selCtrBase = ctrBase
                break

        if verbose:
            print('# Choosing following ctr base with %s occurrences: %s' % (minCount, selCtrBase))

        maxHeight = -1
        selCtr = None
        if minCount == float('inf'):
            selCtr = selCtrBase
        else:
            for ctr in occs[selCtrBase]:
                count = occs[selCtrBase][ctr][0]
                height = occs[selCtrBase][ctr][1]
                if count == minCount and height > maxHeight:
                    maxHeight = height
                    selCtr = ctr

        assert selCtr is not None

        if verbose:
            print('# Choosing following ctr with a height of %d: %s' % (maxHeight, selCtr))

        masksTaken.add(selMask)
        node = getReplacedGraph(node, selMask, selCtr)

        if verbose:
            print('# Replacing %s with %s' % (selCtr, selMask))
            print('# and other occurrences of %s with %s' % (selMask, selCtr))

        node = simplify(node)
        if verifRemoveCstInAddEnable():
            node = removeConstOperandsFromPlus(node)
