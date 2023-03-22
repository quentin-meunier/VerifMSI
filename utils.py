# -*- coding: utf-8 -*-
# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from .config import *
from .node import *


registeredArraysByAddr = {}
registeredArraysByName = {}
registeredArrays = set()
secretShared = set()



def registerArray(name, inWidth, outWidth, addr, size, func, content = None):

    if addr != None:
        if addr in registeredArraysByAddr:
            print('*** Error: Array with base address 0x%x already registered' % addr)
            assert(False)

    if name in registeredArraysByName:
        print('*** Error: Array with name %s already registered' % name)
        assert(False)

    if inWidth != 8 and inWidth != 16 and inWidth != 32:
        print('*** Error: Only supported values for inWidth are 8, 16 and 32')
        assert(False)

    if outWidth != 8 and outWidth != 16 and outWidth != 32:
        print('*** Error: Only supported values for outWidth are 8, 16 and 32')
        assert(False)


    arr = ArrayExp(name, inWidth, outWidth, addr, size, func, content)

    if addr != None:
        registeredArraysByAddr[addr] = arr
    registeredArraysByName[name] = arr
    registeredArrays.add(arr)



def getArrayByAddr(addr):
    return registeredArraysByAddr[addr]

def getArrayByName(name):
    return registeredArraysByName[name]

def getArraySizeByAddr(addr):
    return registeredArraysByAddr[addr].size

def getArraySizeByName(name):
    return registeredArraysByName[name].size

def getArrayFuncByAddr(addr):
    return registeredArraysByAddr[addr].func

def getArrayFuncByName(name):
    return registeredArraysByName[name].func



def getArrayAndOffset(addr):
    from .simplify import simplify
    arr = None
    newChildren = []

    if isinstance(addr, OpNode) and addr.op == '+':
        for child in addr.children:
            if isinstance(child, ConstNode):
                arr = getArrayByAddr(child.cst)
            else:
                newChildren.append(child)
    if arr != None:
        if len(newChildren) == 1:
            offset = newChildren[0]
        else:
            offset = OpNode('+', newChildren)
        if arr.elemSize != 1:
            offset = simplify(LShR(offset, arr.elemSize.bit_length() - 1))

        if offset.width < arr.inWidth:
            offset = ZeroExt(arr.inWidth - offset.width, offset)
        elif offset.width > arr.inWidth:
            # FIXME: verify that all removed bits are 0?
            offset = Extract(arr.inWidth - 1, 0, offset)
        return arr, offset

    # FIXME: in case symbolic array of 32-bit integers is at adress 0x1000,
    # and offset is (k ^ m) + 4, array will be searched at address 0x1004 and it will fail
    # this case will be implemented if encountered
    print('*** Error: symbolic address for symbolic array access does not contain array base address (address is %s)' % addr)
    sys.exit(1)


def getArrayAndOffsetConcrete(addr):
    # FIXME: deal with fully symbolic arrays (return array access from constant index): return arr, offset
    # and semi-symbolic arrays (return constant value from constant index): return None, None
    assert(isinstance(addr, int))
    return None, None

    for arr in registeredArrays:
        if addr >= arr.addr and addr < arr.addr + arr.size:
            offset = (addr - arr.addr) / arr.elemSize
            return arr, Const(offset, arr.inWidth)
    return None, None



def checkResults(res, ref, pei = False, usbv = False):
    from .node import Node
    from .simplify import simplifyCore, equivalence
    assert(isinstance(res, Node))
    assert(isinstance(ref, Node))

    nbBits = ref.width
    
    if nbBits != res.width:
        print('KO (nbBits on res: %d -- expected %d)' % (res.width, nbBits))

    res_s = simplifyCore(res, pei, usbv)
    ref_s = simplifyCore(ref, pei, usbv)

    print('res : %s [%d]' % (res_s, res_s.width))
    print('ref : %s [%d]' % (ref_s, ref_s.width))

    if nbBits != res.width or nbBits != ref.width:
        print('KO (nbBits after simplify: res: %d - ref: %d - expected: %d)' % (res.width, ref.width, nbBits))
    
    if equivalence(res_s, ref_s):
        print('OK')
    else:
        print('KO')
    

def checkTpsResult(exp, expected):
    from .check_leakage import checkTpsVal
    res, t0, t1 = checkTpsVal(exp)
    if res == expected:
        print('OK')
    else:
        print('KO')


def constant(val, width):
    return Const(val, width)


def symbol(name, nature, width):
    return Symb(name, nature, width)


def litteralInteger(e):
    from .simplify import simplify
    if isinstance(e, int):
        return e
    elif isinstance(e, ConstNode):
        return e.cst
    else:
        s = simplify(e)
        if isinstance(s, ConstNode):
            return s.cst
        else:
            return None


def getRealShares(s, nbShares):
    if not isinstance(s, SymbNode) or s.symbType != 'S':
        print('*** Error: first parameter of function getRealShares() can only be a secret variable')
        assert(False)
        sys.exit(1)
    if s in secretShared:
        print('*** Error: Secret variable %s has already been split into shares' % s)
        assert(False)
        sys.exit(1)
    secretShared.add(s)
    pseudoShares = getPseudoSharesInternal(s, nbShares)
    res = []
    for i in range(nbShares):
        a = SymbInternal(s.symb + '[%d]' % i, 'A', s.width, nbShares, s, pseudoShares[i])
        res.append(a)
    return tuple(res)


def getPseudoShares(s, nbShares):
    if not isinstance(s, SymbNode) or s.symbType != 'S':
        print('*** Error: first parameter of function getPseudoShares() can only be a secret variable')
        sys.exit(1)
    if s in secretShared:
        print('*** Error: Secret variable %s has already been split into shares' % s)
        sys.exc_info()[2].print_tb()
        sys.exit(1)
    secretShared.add(s)
    return getPseudoSharesInternal(s, nbShares)


def getPseudoSharesInternal(s, nbShares):
    res = []
    for i in range(0, nbShares - 1):
        a = SymbInternal(s.symb + '@%d' % i, 'M', s.width)
        res.append(a)
    a0 = OpNode('^', [s] + res)
    res.insert(0, a0)
    return tuple(res)


def replaceSharesWithSecretsAndMasks(e):
    def replaceSharesWithSecretsAndMasksRec(node, m):
        if not isinstance(node, OpNode):
            return node
        children = []
        for child in node.children:
            if child in m:
                children.append(m[child])
                continue
            if len(child.shareOcc) != 0:
                newChild = replaceSharesWithSecretsAndMasksRec(child, m)
                children.append(newChild)
                continue
            children.append(child)
        n = OpNode(node.op, children)
        m[node] = n
        return n

    m = {}
    secrets = set()
    for s in e.shareOcc.keys():
        for sh in e.shareOcc[s].keys():
            m[sh] = sh.pseudoShareEq

    return replaceSharesWithSecretsAndMasksRec(e, m)



def width(e):
    return e.width


