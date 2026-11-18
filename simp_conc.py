# -*- coding: utf-8 -*-
# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from .node import Node, OpNode, SymbNode, ConstNode, Extract


def extendedMergeConcatExtract(children):
    currBit = 0
    nextCurrBit = -1
    varWidth = -1
    abortAll = False
    processedNodes = set()

    def traverseExpRec(n):
        nonlocal abortAll, varWidth, nextCurrBit
        if not isinstance(n, OpNode):
            abortAll = True
            return
        if n.op == 'E' and (isinstance(n.children[2], SymbNode) or n.children[2].op == 'A'):
            if not isinstance(n.children[0], ConstNode) or not isinstance(n.children[1], ConstNode):
                abortAll = True
                return
            if n.children[1].cst != currBit:
                abortAll = True
                return
            if varWidth == -1:
                varWidth = n.children[2].width
            elif n.children[2].width != varWidth:
                abortAll = True
                return
            if nextCurrBit == -1:
                nextCurrBit = n.children[0].cst
            elif nextCurrBit != n.children[0].cst:
                abortAll = True
            return
        if n.op not in Node.bitwiseOps:
            abortAll = True
            return
        for child in n.children:
            if child not in processedNodes:
                processedNodes.add(child)
                traverseExpRec(child)
                if abortAll:
                    break

    def traverseExp(n):
        processedNodes.clear()
        traverseExpRec(n)

    m = {}

    def replaceExtractsRec(n):
        if not isinstance(n, OpNode):
            return n
        if n.op == 'E' and (isinstance(n.children[2], SymbNode) or n.children[2].op == 'A'):
            e = Extract(0, 0, n.children[2])
            m[n] = e
            return e
        children_list = []
        for child in n.children:
            if child in m:
                children_list.append(m[child])
            else:
                newChild = replaceExtractsRec(child)
                children_list.append(newChild)
        if children_list == n.children:
            retNode = n
        else:
            assert(n.op != 'E')
            retNode = OpNode(n.op, children_list)
        m[n] = retNode
        return retNode

    def replaceExtracts(n):
        m.clear()
        return replaceExtractsRec(n)

    def buildEquivNodeRec(n):
        if not isinstance(n, OpNode):
            return n
        if n.op == 'E' and (isinstance(n.children[2], SymbNode) or n.children[2].op == 'A'):
            e = n.children[2]
            m[n] = e
            return e
        children_list = []
        for child in n.children:
            if child in m:
                children_list.append(m[child])
            else:
                newChild = buildEquivNodeRec(child)
                children_list.append(newChild)
        assert(n.op != 'E')
        retNode = OpNode(n.op, children_list)
        m[n] = retNode
        return retNode

    def buildEquivNode(n):
        m.clear()
        return buildEquivNodeRec(n)

    def rawEquivalence(node0, node1):
        return node0.h == node1.h

    firstChild = True
    refReplacedChild = None
    for child in children:
        nextCurrBit = -1
        traverseExp(child)
        if abortAll or nextCurrBit == -1:
            return None, False
        if firstChild:
            firstChild = False
            refReplacedChild = replaceExtracts(child)
        else:
            replacedChild = replaceExtracts(child)
            if not rawEquivalence(refReplacedChild, replacedChild):
                return None, False
        currBit = nextCurrBit + 1

    if currBit != varWidth:
        return None, False

    retNode = buildEquivNode(children[0])
    return retNode, True

