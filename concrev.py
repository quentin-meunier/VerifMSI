# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

# Concrete Evaluation

from .utils import *
from .node import *



def getVarsList(*exps):
    allVars = set()
    sharesSubst = {}
    for e in exps:
        #print(' '.join(map(lambda x: '%s' % x.symb, e.shareOcc.keys())))
        allVars.update(list(e.maskingMaskOcc) + list(e.otherMaskOcc) + list(e.secretVarOcc) + list(e.publicVarOcc))
        for origSecret in e.shareOcc.keys():
            allVars.update(e.shareOcc[origSecret])

    secretsToRemove = set() # contains secrets to remove because there are occurrences of shares of this secret in one of the expressions, and the value of the secret must thus be determined by the shares
    secretNbShares = {}
    for v in allVars:
        if v.symbType == 'A' and v.origSecret in allVars and v.origSecret not in secretsToRemove:
            secretsToRemove.add(v.origSecret)
            secretNbShares[v.origSecret] = v.nbShares

    for s in secretsToRemove:
        assert(s in allVars)
        # process only once each secret if several shares of it are in secretsToRemove
        allVars.remove(s)
        shares = []
        for i in range(secretNbShares[s]):
            # No need to specify the 3 last parameters as this call is expected to return an already existing share node
            shares.append(SymbInternal(s.symb + '[%d]' % i, 'A', s.width))

        allShares = shares[0]
        for i in range(1, secretNbShares[s]):
            allShares ^= shares[i]
        sharesSubst[s] = allShares


    allVarsNoBits = set()
    for n in allVars:
        if '#' in n.symb:
            import re
            varName, b = re.split(r'#', n.symb)
            allVarsNoBits.add(Node.symb2node[varName])
        else:
            allVarsNoBits.add(n)

    allVarsList = sorted(list(allVarsNoBits), key = lambda x: x.symb)
    return allVarsList, sharesSubst
 


def getExpValue(node, m):
    return getExpValueRec(node, m, {})


def getExpValueRec(node, m, expCache):
    if isinstance(node, SymbNode):
        if node in m:
            return m[node]
        if '#' in node.symb:
            import re
            n, b = re.split(r'#', node.symb)
            node = Node.symb2node[n]
            bit = int(b)
            if node in m:
                return Extract(bit, bit, m[node])
        print('*** Error: Value for symbol %s not specified' % node.symb)
        sys.exit(1)

    if isinstance(node, ConstNode):
        return node

    if isinstance(node, StrNode):
        return node

    if node in expCache:
        return expCache[node]

    newChildren = []
    op = node.op
    for child in node.children:
        newChildren.append(getExpValue(child, m))
 
    for child in newChildren:
        assert(isinstance(child, ConstNode) or isinstance(child, StrNode))

    if op == 'E':
        res = Extract(*newChildren)
    elif op == 'ZE':
        res = ZeroExt(*newChildren)
    elif op == 'SE':
        res = SignExt(*newChildren)
    elif op == 'C':
        res = Concat(*newChildren[::-1])
    elif op == 'LS':
        res = LShR(*newChildren)
    elif op == '>>':
        res = newChildren[0] >> newChildren[1]
    elif op == '<<':
        res = newChildren[0] << newChildren[1]
    elif op == '-':
        res = -newChildren[0]
    elif op == 'A':
        if ArrayExp.allArrays[newChildren[0].strn].content == None:
            print('*** Error: concrete evaluation of an array access is only possible with an initialized content' % node.symb)
            sys.exit(1)
        res = Const(ArrayExp.allArrays[newChildren[0].strn].content[newChildren[1].cst], ArrayExp.allArrays[newChildren[0].strn].outWidth)
    else:
        if op == '&':
            res = ~0
        else:
            res = 0
        for child in newChildren:
            if op == '^':
                res = res ^ child.cst
            elif op == '&':
                res = res & child.cst
            elif op == '|':
                res = res | child.cst
            elif op == '~':
                res = (1 << node.width) - 1 - child.cst
            elif op == '+':
                res = (res + child.cst) % (1 << node.width)
            else:
                assert(False)
        res = Const(res, node.width)

    expCache[node] = res
    return res




def compareExpsWithExevRec(e0, e1, allVars, sharesSubst, idx, m):
    if idx < len(allVars):
        var = allVars[idx]
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            res, v0, v1 = compareExpsWithExevRec(e0, e1, allVars, sharesSubst, idx + 1, m)
            if res != None:
                return res, v0, v1
            m[var] = None
        return None, None, None
    else:
        for s in sharesSubst:
            m[s] = getExpValue(sharesSubst[s], m)
        v0 = getExpValue(e0, m)
        v1 = getExpValue(e1, m)
        if v0.cst == v1.cst and v0.width == v1.width:
            return None, None, None
        else:
            return dict(m), v0.cst, v1.cst



def compareExpsWithExev(e0, e1):
    allVarsList, sharesSubst = getVarsList(e0, e1)
    return compareExpsWithExevRec(e0, e1, allVarsList, sharesSubst, 0, {})



def compareExpsWithRandev(e0, e1, nbEval):
    # Random Evaluations
    import random

    allVarsList, sharesSubst = getVarsList(e0, e1)
    for i in range(nbEval):
        m = {}
        for v in allVarsList:
            m[v] = Const(random.randrange(0, (1 << v.width)), v.width)
        for s in sharesSubst:
            m[s] = getExpValue(sharesSubst[s], m)

        v0 = getExpValue(e0, m)
        v1 = getExpValue(e1, m)
        if v0.cst != v1.cst or v0.width != v1.width:
            return m, v0, v1
    return None, None, None




def getDistribRefBis(e0, distribRef, nonSecretVars, idx, m):
    if idx < len(nonSecretVars):
        var = nonSecretVars[idx]
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            getDistribRefBis(e0, distribRef, nonSecretVars, idx + 1, m)
    else:
        v = getExpValue(e0, m).cst
        distribRef[v] += 1


def getDistribRef(e0, secretVars, nonSecretVars):
    m = {}
    for k in secretVars:
        m[k] = Const(0, k.width)

    distribRef = {}
    for v in range(1 << e0.width):
        distribRef[v] = 0
    getDistribRefBis(e0, distribRef, nonSecretVars, 0, m)
    return distribRef


def getDistribWithExevRecBis(e0, distrib, distribRef, nonSecretVars, idx, m):
    if idx < len(nonSecretVars):
        var = nonSecretVars[idx]
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            getDistribWithExevRecBis(e0, distrib, distribRef, nonSecretVars, idx + 1, m)
    else:
        v = getExpValue(e0, m).cst
        distrib[v] += 1


def getDistribWithExevRec(e0, distribRef, secretVars, nonSecretVars, idx, m):
    if idx < len(secretVars):
        var = secretVars[idx]
        allRud = True
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            rud, sid = getDistribWithExevRec(e0, distribRef, secretVars, nonSecretVars, idx + 1, m)
            if not sid:
                return False, False
            allRud = allRud and rud
        return allRud, True
    else:
        distrib = {}
        for v in range(1 << e0.width):
            distrib[v] = 0
        getDistribWithExevRecBis(e0, distrib, distribRef, nonSecretVars, 0, m)
        rud = True
        for v in range(1 << e0.width):
            if distrib[v] != distribRef[0]:
                rud = False
            if distrib[v] != distribRef[v]:
                return False, False
        return rud, True



def getDistribWithExev(e):
    e0 = replaceSharesWithSecretsAndMasks(e)
    allVarsList, sharesSubst = getVarsList(e0)

    secretVars = list(filter(lambda x: x.symbType == 'S', allVarsList))
    nonSecretVars = list(filter(lambda x: x.symbType != 'S', allVarsList))

    distribRef = getDistribRef(e0, secretVars, nonSecretVars)
    rud, sid = getDistribWithExevRec(e0, distribRef, secretVars, nonSecretVars, 0, {})

    return rud, sid




