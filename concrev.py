# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

import sys
import random

from .utils import *
from .node import *
from .config import TPS, NI, SNI, RNI, PINI, OPINI
from .simplify import getBitDecomposition


class RudRef:
    def __init__(self, val=False):
        self.val = bool(val)

    def __bool__(self):
        return bool(self.val)

    def __repr__(self):
        return str(self.val)


# Global instances for C++ style tests like `rud; sid = getDistribWithExev(e, rud)`
rud = RudRef(False)
sid = False
res = False


class CompareResult:
    def __init__(self, is_equal, res_map=None, v0=None, v1=None):
        self.is_equal = bool(is_equal)
        self.res_map = res_map
        self.v0 = v0
        self.v1 = v1

    def __bool__(self):
        return self.is_equal

    def __iter__(self):
        return iter((self.res_map, self.v0, self.v1))

    def __repr__(self):
        return 'True' if self.is_equal else 'False'


class CheckDistribResult:
    def __init__(self, sid_val, rud_val):
        self.sid = bool(sid_val)
        self.rud = bool(rud_val)

    def __bool__(self):
        return self.sid

    def __iter__(self):
        return iter((self.rud, self.sid))

    def __repr__(self):
        return f"(rud={self.rud}, sid={self.sid})"


def secPropValidity(node, secProp):
    if isinstance(node, (list, tuple, set)):
        for n in node:
            secPropValidity(n, secProp)
        return
    if secProp == TPS:
        if len(node.shareOcc) != 0:
            print('*** Error: TPS verification should not use a share representation but explicit secret variables and masks')
            sys.exit(1)
    else:
        if len(node.secretVarOcc) != 0:
            propName = 'NI' if secProp == NI else ('RNI' if secProp == RNI else ('PINI' if secProp == PINI else 'OPINI'))
            print(f'*** Error: {propName} verification should use a share representation and not explicit secret variables')
            sys.exit(1)


def getVarsList(exps, allVarsVec=None):
    allVars = set()
    for e in exps:
        for k in e.maskingMaskOcc.keys():
            allVars.add(k)
        for k in e.otherMaskOcc.keys():
            allVars.add(k)
        for k in e.secretVarOcc.keys():
            allVars.add(k)
        for k in e.publicVarOcc.keys():
            allVars.add(k)
        for v in e.shareOcc.values():
            for l in v.keys():
                allVars.add(l)

    for n in allVars:
        if n.width != 1:
            print('*** Internal Error: variables found for exhaustive evaluation should all be 1-bit wide')
            assert False

    res = sorted(list(allVars), key=lambda x: x.symb)
    if allVarsVec is not None:
        allVarsVec.clear()
        allVarsVec.extend(res)
    return res


class FastInstr:
    def __init__(self, op, outReg, width=0, inReg1=-1, inReg2=-1, cstVal=0, arrayName=None, multiIn=None, childWidths=None):
        self.op = op
        self.outReg = outReg
        self.width = width
        self.inReg1 = inReg1
        self.inReg2 = inReg2
        self.cstVal = cstVal
        self.arrayName = arrayName
        self.multiIn = multiIn or []
        self.childWidths = childWidths or []


class FastCircuit:
    def __init__(self):
        self.code = []
        self.var2reg = {}
        self.node2reg = {}
        self.numRegs = 0
        self.outReg = -1
        self.isBitsliceable = True

    def compileNode(self, n):
        if n in self.node2reg:
            return self.node2reg[n]

        if isinstance(n, ConstNode):
            r = self.numRegs
            self.numRegs += 1
            self.node2reg[n] = r
            instr = FastInstr('CONST', r, width=n.width, cstVal=n.cst)
            self.code.append(instr)
            return r

        if isinstance(n, StrNode):
            r = self.numRegs
            self.numRegs += 1
            self.node2reg[n] = r
            instr = FastInstr('CONST', r, width=0, cstVal=0, arrayName=n.strn)
            self.code.append(instr)
            self.isBitsliceable = False
            return r

        if isinstance(n, SymbNode):
            if n in self.var2reg:
                r = self.var2reg[n]
                self.node2reg[n] = r
                return r
            r = self.numRegs
            self.numRegs += 1
            self.var2reg[n] = r
            self.node2reg[n] = r
            instr = FastInstr('VAR', r, width=n.width)
            self.code.append(instr)
            return r

        childRegs = []
        childWidths = []
        if n.children is not None:
            for c in n.children:
                childRegs.append(self.compileNode(c))
                childWidths.append(c.width)

        r = self.numRegs
        self.numRegs += 1
        self.node2reg[n] = r

        op = n.op
        if op == '^':
            instr = FastInstr('BXOR', r, width=n.width, multiIn=childRegs)
        elif op == '&':
            instr = FastInstr('BAND', r, width=n.width, multiIn=childRegs)
        elif op == '|':
            instr = FastInstr('BOR', r, width=n.width, multiIn=childRegs)
        elif op == '~':
            instr = FastInstr('BNOT', r, width=n.width, inReg1=childRegs[0])
        elif op in ('>>', 'LS', 's>>', 'SLS'):
            instr = FastInstr('LSHR', r, width=n.width, inReg1=childRegs[0], inReg2=childRegs[1])
            self.isBitsliceable = False
        elif op in ('<<', 's<<'):
            instr = FastInstr('LSHL', r, width=n.width, inReg1=childRegs[0], inReg2=childRegs[1])
            self.isBitsliceable = False
        elif op == '+':
            instr = FastInstr('PLUS', r, width=n.width, multiIn=childRegs)
            self.isBitsliceable = False
        elif op == '-':
            instr = FastInstr('UMINUS', r, width=n.width, inReg1=childRegs[0])
            self.isBitsliceable = False
        elif op in ('*', '**'):
            instr = FastInstr('IMUL', r, width=n.width, multiIn=childRegs)
            self.isBitsliceable = False
        elif op in ('M', 'P'):
            instr = FastInstr('GMUL', r, width=n.width, multiIn=childRegs)
            self.isBitsliceable = False
        elif op == 'E':
            instr = FastInstr('EXTRACT', r, width=n.width, inReg1=childRegs[0], inReg2=childRegs[1], multiIn=[childRegs[2]])
            if n.width != 1 or childWidths[2] != 1:
                self.isBitsliceable = False
        elif op == 'ZE':
            instr = FastInstr('ZEXT', r, width=n.width, inReg1=childRegs[0], inReg2=childRegs[1])
            self.isBitsliceable = False
        elif op == 'SE':
            origW = childWidths[1]
            instr = FastInstr('SEXT', r, width=n.width, inReg1=origW, inReg2=childRegs[1])
            self.isBitsliceable = False
        elif op == 'C':
            instr = FastInstr('CONCAT', r, width=n.width, multiIn=childRegs, childWidths=childWidths)
            self.isBitsliceable = False
        elif op == 'A':
            arrayName = n.children[0].strn
            instr = FastInstr('ARRAY', r, width=n.width, inReg1=childRegs[0], inReg2=childRegs[1], arrayName=arrayName)
            self.isBitsliceable = False
        else:
            raise ValueError(f"Unsupported op: {op}")

        self.code.append(instr)
        return r

    def compile(self, root):
        self.code = []
        self.var2reg = {}
        self.node2reg = {}
        self.numRegs = 0
        self.isBitsliceable = (root.width == 1)
        self.outReg = self.compileNode(root)

    def eval_scalar(self, regs):
        for instr in self.code:
            op = instr.op
            outR = instr.outReg
            if op == 'VAR':
                continue
            elif op == 'CONST':
                regs[outR] = instr.cstVal
            elif op == 'BXOR':
                v = 0
                for inR in instr.multiIn:
                    v ^= regs[inR]
                regs[outR] = v
            elif op == 'BAND':
                w = instr.width
                v = (1 << w) - 1
                for inR in instr.multiIn:
                    v &= regs[inR]
                regs[outR] = v
            elif op == 'BOR':
                v = 0
                for inR in instr.multiIn:
                    v |= regs[inR]
                regs[outR] = v
            elif op == 'BNOT':
                w = instr.width
                mask = (1 << w) - 1
                regs[outR] = (~regs[instr.inReg1]) & mask
            elif op == 'LSHR':
                regs[outR] = regs[instr.inReg1] >> regs[instr.inReg2]
            elif op == 'LSHL':
                w = instr.width
                mask = (1 << w) - 1
                regs[outR] = (regs[instr.inReg1] << regs[instr.inReg2]) & mask
            elif op == 'PLUS':
                w = instr.width
                mask = (1 << w) - 1
                s = 0
                for inR in instr.multiIn:
                    s += regs[inR]
                regs[outR] = s & mask
            elif op == 'UMINUS':
                w = instr.width
                mask = (1 << w) - 1
                regs[outR] = (-regs[instr.inReg1]) & mask
            elif op == 'IMUL':
                w = instr.width
                mask = (1 << w) - 1
                p = 1
                for inR in instr.multiIn:
                    p *= regs[inR]
                regs[outR] = p & mask
            elif op == 'GMUL':
                p = 1
                for inR in instr.multiIn:
                    p = gmulInt(p, regs[inR])
                regs[outR] = p & 0xFF
            elif op == 'EXTRACT':
                high = regs[instr.inReg1]
                low = regs[instr.inReg2]
                val = regs[instr.multiIn[0]]
                w = high - low + 1
                mask = (1 << w) - 1
                regs[outR] = (val >> low) & mask
            elif op == 'ZEXT':
                regs[outR] = regs[instr.inReg2]
            elif op == 'SEXT':
                val = regs[instr.inReg2]
                origW = instr.inReg1
                sign = (val >> (origW - 1)) & 1
                if sign:
                    top = (1 << instr.width) - (1 << origW)
                    val |= top
                regs[outR] = val
            elif op == 'CONCAT':
                val = 0
                shift = 0
                for i in range(len(instr.multiIn) - 1, -1, -1):
                    inR = instr.multiIn[i]
                    cw = instr.childWidths[i]
                    cmask = (1 << cw) - 1
                    val |= ((regs[inR] & cmask) << shift)
                    shift += cw
                regs[outR] = val
            elif op == 'ARRAY':
                arr = ArrayExp.allArrays[instr.arrayName]
                regs[outR] = arr.getContent(regs[instr.inReg2])
        return regs[self.outReg]

    def eval_bitsliced(self, regs):
        for instr in self.code:
            op = instr.op
            outR = instr.outReg
            if op == 'VAR':
                continue
            elif op == 'CONST':
                regs[outR] = 0xFFFFFFFFFFFFFFFF if instr.cstVal else 0
            elif op == 'BXOR':
                v = 0
                for inR in instr.multiIn:
                    v ^= regs[inR]
                regs[outR] = v & 0xFFFFFFFFFFFFFFFF
            elif op == 'BAND':
                v = 0xFFFFFFFFFFFFFFFF
                for inR in instr.multiIn:
                    v &= regs[inR]
                regs[outR] = v & 0xFFFFFFFFFFFFFFFF
            elif op == 'BOR':
                v = 0
                for inR in instr.multiIn:
                    v |= regs[inR]
                regs[outR] = v & 0xFFFFFFFFFFFFFFFF
            elif op == 'BNOT':
                regs[outR] = (~regs[instr.inReg1]) & 0xFFFFFFFFFFFFFFFF
            elif op == 'EXTRACT':
                regs[outR] = regs[instr.multiIn[0]]
            else:
                assert False, f"Unexpected bitsliced op: {op}"
        return regs[self.outReg]


PATTERNS = [
    0xAAAAAAAAAAAAAAAA,
    0xCCCCCCCCCCCCCCCC,
    0xF0F0F0F0F0F0F0F0,
    0xFF00FF00FF00FF00,
    0xFFFF0000FFFF0000,
    0xFFFFFFFF00000000
]


def fastGetDistrib(fc, maskRegs, regs, outWidth):
    numMasks = len(maskRegs)
    if fc.isBitsliceable and outWidth == 1:
        if numMasks == 0:
            out = fc.eval_bitsliced(regs)
            if out & 1:
                return [0, 1]
            else:
                return [1, 0]
        if numMasks <= 6:
            activeCount = 1 << numMasks
            activeMask = (1 << activeCount) - 1 if activeCount < 64 else 0xFFFFFFFFFFFFFFFF
            for i in range(numMasks):
                regs[maskRegs[i]] = PATTERNS[i] & activeMask
            out = fc.eval_bitsliced(regs) & activeMask
            ones = bin(out).count('1')
            return [activeCount - ones, ones]

        numBlocks = 1 << (numMasks - 6)
        for i in range(6):
            regs[maskRegs[i]] = PATTERNS[i]
        ones = 0
        for b in range(numBlocks):
            for i in range(6, numMasks):
                regs[maskRegs[i]] = 0xFFFFFFFFFFFFFFFF if ((b >> (i - 6)) & 1) else 0
            out = fc.eval_bitsliced(regs)
            ones += bin(out).count('1')
        total = 1 << numMasks
        return [total - ones, ones]
    else:
        distrib = [0] * (1 << outWidth)
        for mval in range(1 << numMasks):
            for i in range(numMasks):
                regs[maskRegs[i]] = (mval >> i) & 1
            out = fc.eval_scalar(regs)
            distrib[out] += 1
        return distrib


def fastCompareExpsWithExevRec(fc0, fc1, varRegs0, varRegs1, allVars, idx, regs0, regs1, res_map):
    if idx < len(allVars):
        r0 = varRegs0[idx]
        r1 = varRegs1[idx]
        for val in (0, 1):
            if r0 >= 0:
                regs0[r0] = val
            if r1 >= 0:
                regs1[r1] = val
            retval = fastCompareExpsWithExevRec(fc0, fc1, varRegs0, varRegs1, allVars, idx + 1, regs0, regs1, res_map)
            if not retval:
                return False
        return True
    else:
        val0 = fc0.eval_scalar(regs0)
        val1 = fc1.eval_scalar(regs1)
        if val0 == val1:
            return True
        else:
            for i in range(len(allVars)):
                v = regs0[varRegs0[i]] if varRegs0[i] >= 0 else regs1[varRegs1[i]]
                res_map[allVars[i]] = Const(v, allVars[i].width)
            res_map['_v0'] = val0
            res_map['_v1'] = val1
            return False


def compareExpsWithExev(e0, e1):
    if e0.width != e1.width:
        return CompareResult(False)
    assert e0.width <= 64
    e0r = replaceSharesWithSecretsAndMasks(e0)
    e1r = replaceSharesWithSecretsAndMasks(e1)
    e0b = getBitDecomposition(e0r)
    e1b = getBitDecomposition(e1r)
    allVarsVec = []
    getVarsList([e0b, e1b], allVarsVec)
    fc0 = FastCircuit()
    fc1 = FastCircuit()
    fc0.compile(e0b)
    fc1.compile(e1b)
    varRegs0 = [fc0.var2reg.get(v, -1) for v in allVarsVec]
    varRegs1 = [fc1.var2reg.get(v, -1) for v in allVarsVec]
    regs0 = [0] * fc0.numRegs
    regs1 = [0] * fc1.numRegs
    res_map = {}
    is_eq = fastCompareExpsWithExevRec(fc0, fc1, varRegs0, varRegs1, allVarsVec, 0, regs0, regs1, res_map)
    if is_eq:
        return CompareResult(True, None, None, None)
    else:
        v0 = res_map.pop('_v0', 0)
        v1 = res_map.pop('_v1', 0)
        return CompareResult(False, res_map, v0, v1)


def compareExpsWithRandev(e0, e1, nbEval):
    if e0.width != e1.width:
        return CompareResult(False)
    e0r = replaceSharesWithSecretsAndMasks(e0)
    e1r = replaceSharesWithSecretsAndMasks(e1)
    e0b = getBitDecomposition(e0r)
    e1b = getBitDecomposition(e1r)
    allVarsVec = []
    getVarsList([e0b, e1b], allVarsVec)
    fc0 = FastCircuit()
    fc1 = FastCircuit()
    fc0.compile(e0b)
    fc1.compile(e1b)
    varRegs0 = [fc0.var2reg.get(v, -1) for v in allVarsVec]
    varRegs1 = [fc1.var2reg.get(v, -1) for v in allVarsVec]
    regs0 = [0] * fc0.numRegs
    regs1 = [0] * fc1.numRegs
    for _ in range(nbEval):
        for vi in range(len(allVarsVec)):
            val = random.getrandbits(1)
            if varRegs0[vi] >= 0:
                regs0[varRegs0[vi]] = val
            if varRegs1[vi] >= 0:
                regs1[varRegs1[vi]] = val
        val0 = fc0.eval_scalar(regs0)
        val1 = fc1.eval_scalar(regs1)
        if val0 != val1:
            res_map = {}
            for vi in range(len(allVarsVec)):
                v = regs0[varRegs0[vi]] if varRegs0[vi] >= 0 else regs1[varRegs1[vi]]
                res_map[allVarsVec[vi]] = Const(v, allVarsVec[vi].width)
            return CompareResult(False, res_map, val0, val1)
    return CompareResult(True, None, None, None)


def fastGetDistribWithExevRec(fc, distribRef, secretRegs, maskRegs, idx, regs, outWidth, rud_holder):
    if idx < len(secretRegs):
        r = secretRegs[idx]
        if r >= 0:
            regs[r] = 0
            if not fastGetDistribWithExevRec(fc, distribRef, secretRegs, maskRegs, idx + 1, regs, outWidth, rud_holder):
                return False
            regs[r] = 0xFFFFFFFFFFFFFFFF if (fc.isBitsliceable and outWidth == 1) else 1
            return fastGetDistribWithExevRec(fc, distribRef, secretRegs, maskRegs, idx + 1, regs, outWidth, rud_holder)
        else:
            return fastGetDistribWithExevRec(fc, distribRef, secretRegs, maskRegs, idx + 1, regs, outWidth, rud_holder)
    else:
        distrib = fastGetDistrib(fc, maskRegs, regs, outWidth)
        for v in range(len(distrib)):
            if distrib[v] != distribRef[0]:
                rud_holder[0] = False
            if distrib[v] != distribRef[v]:
                return False
        return True


def fastEnumeratePublicVarsRec(fc, publicRegs, secretRegs, maskRegs, idx, regs, outWidth, rud_holder):
    if idx < len(publicRegs):
        r = publicRegs[idx]
        if r >= 0:
            regs[r] = 0
            if not fastEnumeratePublicVarsRec(fc, publicRegs, secretRegs, maskRegs, idx + 1, regs, outWidth, rud_holder):
                return False
            regs[r] = 0xFFFFFFFFFFFFFFFF if (fc.isBitsliceable and outWidth == 1) else 1
            return fastEnumeratePublicVarsRec(fc, publicRegs, secretRegs, maskRegs, idx + 1, regs, outWidth, rud_holder)
        else:
            return fastEnumeratePublicVarsRec(fc, publicRegs, secretRegs, maskRegs, idx + 1, regs, outWidth, rud_holder)
    else:
        for sr in secretRegs:
            if sr >= 0:
                regs[sr] = 0
        distribRef = fastGetDistrib(fc, maskRegs, regs, outWidth)
        rudLocal = [True]
        res = fastGetDistribWithExevRec(fc, distribRef, secretRegs, maskRegs, 0, regs, outWidth, rudLocal)
        if not rudLocal[0] or not res:
            rud_holder[0] = False
        return res


def getDistribWithExev(e, rud_arg=None):
    assert e.width <= 64
    secPropValidity(e, TPS)
    e0 = getBitDecomposition(e)
    allVarsVec = []
    getVarsList([e0], allVarsVec)
    fc = FastCircuit()
    fc.compile(e0)
    secretRegs = []
    publicRegs = []
    maskRegs = []
    for v in allVarsVec:
        r = fc.var2reg.get(v, -1)
        if v.symbType == 'S':
            if r >= 0:
                secretRegs.append(r)
        elif v.symbType == 'P':
            if r >= 0:
                publicRegs.append(r)
        else:
            assert v.symbType == 'M'
            if r >= 0:
                maskRegs.append(r)
    regs = [0] * fc.numRegs
    rud_holder = [True]
    res_sid = fastEnumeratePublicVarsRec(fc, publicRegs, secretRegs, maskRegs, 0, regs, e0.width, rud_holder)
    rud_val = rud_holder[0]
    if isinstance(rud_arg, RudRef):
        rud_arg.val = rud_val
    return CheckDistribResult(res_sid, rud_val)


def isTPSWithExev(e):
    return bool(getDistribWithExev(e, RudRef(False)))


def fastShareIsEffective(fc, sharesWithFixedValRegs, sReg, maskRegs, idx, regs, outWidth):
    if idx < len(sharesWithFixedValRegs):
        r = sharesWithFixedValRegs[idx]
        regs[r] = 0
        if fastShareIsEffective(fc, sharesWithFixedValRegs, sReg, maskRegs, idx + 1, regs, outWidth):
            return True
        regs[r] = 0xFFFFFFFFFFFFFFFF if (fc.isBitsliceable and outWidth == 1) else 1
        return fastShareIsEffective(fc, sharesWithFixedValRegs, sReg, maskRegs, idx + 1, regs, outWidth)
    else:
        regs[sReg] = 0
        distrib0 = fastGetDistrib(fc, maskRegs, regs, outWidth)
        regs[sReg] = 0xFFFFFFFFFFFFFFFF if (fc.isBitsliceable and outWidth == 1) else 1
        distrib1 = fastGetDistrib(fc, maskRegs, regs, outWidth)
        for v in range(len(distrib0)):
            if distrib0[v] != distrib1[v]:
                return True
        return False


def fastGetEffectiveShares(fc, publicRegs, shareVars, maskRegs, idx, regs, outWidth, effectiveShares):
    if idx < len(publicRegs):
        r = publicRegs[idx]
        regs[r] = 0
        fastGetEffectiveShares(fc, publicRegs, shareVars, maskRegs, idx + 1, regs, outWidth, effectiveShares)
        regs[r] = 0xFFFFFFFFFFFFFFFF if (fc.isBitsliceable and outWidth == 1) else 1
        fastGetEffectiveShares(fc, publicRegs, shareVars, maskRegs, idx + 1, regs, outWidth, effectiveShares)
    else:
        for s in shareVars:
            if s not in effectiveShares:
                if s not in fc.var2reg:
                    continue
                sReg = fc.var2reg[s]
                sharesWithFixedVal = []
                for rs in shareVars:
                    if rs != s and rs in fc.var2reg:
                        sharesWithFixedVal.append(fc.var2reg[rs])
                sIsEffective = fastShareIsEffective(fc, sharesWithFixedVal, sReg, maskRegs, 0, regs, outWidth)
                if sIsEffective:
                    effectiveShares.add(s)


def isNIWithExev(e, maxShareOcc):
    assert e.width <= 64
    secPropValidity(e, NI)
    e0 = getBitDecomposition(e)
    allVarsVec = []
    getVarsList([e0], allVarsVec)
    shareVarsOrig = []
    shareVars = []
    publicVars = []
    maskVars = []
    secretVars = set()
    for v in allVarsVec:
        if v.symbType == 'A':
            shareVarsOrig.append(v)
        elif v.symbType == 'P':
            publicVars.append(v)
        else:
            assert v.symbType == 'M'
            maskVars.append(v)
    for v in shareVarsOrig:
        secretVars.add(v.origSecret)
    for v in secretVars:
        nbShares = sum(1 for sh in shareVarsOrig if sh.origSecret == v)
        if nbShares > maxShareOcc:
            for sh in shareVarsOrig:
                if sh.origSecret == v:
                    shareVars.append(sh)
        else:
            for sh in shareVarsOrig:
                if sh.origSecret == v:
                    publicVars.append(sh)
    fc = FastCircuit()
    fc.compile(e0)
    publicRegs = [fc.var2reg[pv] for pv in publicVars if pv in fc.var2reg]
    maskRegs = [fc.var2reg[mv] for mv in maskVars if mv in fc.var2reg]
    regs = [0] * fc.numRegs
    effectiveShares = set()
    fastGetEffectiveShares(fc, publicRegs, shareVars, maskRegs, 0, regs, e0.width, effectiveShares)
    for s in secretVars:
        nbEffectiveShares = sum(1 for sh in shareVars if sh.origSecret == s and sh in effectiveShares)
        if nbEffectiveShares > maxShareOcc:
            return False
    return True


def isRNIWithExev(e, diff):
    assert e.width <= 64
    secPropValidity(e, RNI)
    e0 = getBitDecomposition(e)
    allVarsVec = []
    getVarsList([e0], allVarsVec)
    shareVarsOrig = []
    shareVars = []
    publicVars = []
    maskVars = []
    secretVars = set()
    for v in allVarsVec:
        if v.symbType == 'A':
            shareVarsOrig.append(v)
        elif v.symbType == 'P':
            publicVars.append(v)
        else:
            assert v.symbType == 'M'
            maskVars.append(v)
    for v in shareVarsOrig:
        secretVars.add(v.origSecret)
    for v in secretVars:
        nbUsedShares = sum(1 for sh in shareVarsOrig if sh.origSecret == v)
        nbTotalShares = v.nbShares
        assert nbUsedShares == len(e0.shareOcc[v])
        if nbUsedShares + diff >= nbTotalShares:
            for sh in shareVarsOrig:
                if sh.origSecret == v:
                    shareVars.append(sh)
        else:
            for sh in shareVarsOrig:
                if sh.origSecret == v:
                    publicVars.append(sh)
    fc = FastCircuit()
    fc.compile(e0)
    publicRegs = [fc.var2reg[pv] for pv in publicVars if pv in fc.var2reg]
    maskRegs = [fc.var2reg[mv] for mv in maskVars if mv in fc.var2reg]
    regs = [0] * fc.numRegs
    effectiveShares = set()
    fastGetEffectiveShares(fc, publicRegs, shareVars, maskRegs, 0, regs, e0.width, effectiveShares)
    for s in secretVars:
        nbTotalShares = s.nbShares
        nbEffectiveShares = sum(1 for sh in shareVars if sh.origSecret == s and sh in effectiveShares)
        if nbEffectiveShares + diff >= nbTotalShares:
            return False
    return True


def isPINIWithExev(e, maxShareOcc, outputIndexes):
    assert e.width <= 64
    secPropValidity(e, PINI)
    e0 = getBitDecomposition(e)
    allVarsVec = []
    getVarsList([e0], allVarsVec)
    shareVars = []
    publicVars = []
    maskVars = []
    secretVars = set()
    for v in allVarsVec:
        if v.symbType == 'A':
            shareVars.append(v)
        elif v.symbType == 'P':
            publicVars.append(v)
        else:
            assert v.symbType == 'M'
            maskVars.append(v)
    for v in shareVars:
        secretVars.add(v.origSecret)
    fc = FastCircuit()
    fc.compile(e0)
    publicRegs = [fc.var2reg[pv] for pv in publicVars if pv in fc.var2reg]
    maskRegs = [fc.var2reg[mv] for mv in maskVars if mv in fc.var2reg]
    regs = [0] * fc.numRegs
    effectiveShares = set()
    fastGetEffectiveShares(fc, publicRegs, shareVars, maskRegs, 0, regs, e0.width, effectiveShares)
    effectiveShareIndexesNotInOutputIndexes = set()
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    for sh in effectiveShares:
        if sh.shareNum not in outputIndexes:
            effectiveShareIndexesNotInOutputIndexes.add(sh.shareNum)
    return len(effectiveShareIndexesNotInOutputIndexes) <= maxShareOcc


def isOPINIWithExev(e, maxShareOcc, outputIndexes, additionalInputIndexes=None):
    assert e.width <= 64
    secPropValidity(e, OPINI)
    e0 = getBitDecomposition(e)
    allVarsVec = []
    getVarsList([e0], allVarsVec)
    shareVars = []
    publicVars = []
    maskVars = []
    secretVars = set()
    for v in allVarsVec:
        if v.symbType == 'A':
            shareVars.append(v)
        elif v.symbType == 'P':
            publicVars.append(v)
        else:
            assert v.symbType == 'M'
            maskVars.append(v)
    for v in shareVars:
        secretVars.add(v.origSecret)
    fc = FastCircuit()
    fc.compile(e0)
    publicRegs = [fc.var2reg[pv] for pv in publicVars if pv in fc.var2reg]
    maskRegs = [fc.var2reg[mv] for mv in maskVars if mv in fc.var2reg]
    regs = [0] * fc.numRegs
    effectiveShares = set()
    fastGetEffectiveShares(fc, publicRegs, shareVars, maskRegs, 0, regs, e0.width, effectiveShares)
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    if additionalInputIndexes is None:
        additionalInputIndexes = set()
    for sh in effectiveShares:
        if sh.shareNum not in outputIndexes:
            additionalInputIndexes.add(sh.shareNum)
    return len(additionalInputIndexes) <= maxShareOcc


def getExpValue(node, m):
    return getExpValueRec(node, m, {})


def getExpValueRec(node, m, expCache):
    if isinstance(node, SymbNode):
        if node in m:
            return m[node]
        if '#' in node.symb:
            import re
            n, b = re.split(r'#', node.symb)
            node_base = Node.symbolsByName.get(n) or Node.symb2node.get(n)
            bit = int(b)
            if node_base in m:
                return Extract(bit, bit, m[node_base])
        print(f"*** Error: Value for symbol {node.symb} not specified")
        sys.exit(1)

    if isinstance(node, ConstNode) or isinstance(node, StrNode):
        return node

    if node in expCache:
        return expCache[node]

    newChildren = [getExpValueRec(child, m, expCache) for child in node.children]

    for child in newChildren:
        assert isinstance(child, (ConstNode, StrNode))

    op = node.op
    if op == 'E':
        res = Extract(*newChildren)
    elif op == 'ZE':
        res = ZeroExt(*newChildren)
    elif op == 'SE':
        res = SignExt(*newChildren)
    elif op == 'C':
        res = Concat(*newChildren[::-1])
    elif op in ('LS', '>>', 's>>', 'SLS'):
        res = LShR(*newChildren)
    elif op in ('<<', 's<<'):
        res = newChildren[0] << newChildren[1]
    elif op == '-':
        res = -newChildren[0]
    elif op == 'A':
        arr = ArrayExp.allArrays[newChildren[0].strn]
        if arr.content is None:
            print('*** Error: concrete evaluation of an array access is only possible with an initialized content')
            sys.exit(1)
        res = Const(arr.getContent(newChildren[1].cst), arr.outWidth)
    elif op == '+':
        s = sum(c.cst for c in newChildren) % (1 << node.width)
        res = Const(s, node.width)
    elif op == '*':
        p = 1
        for c in newChildren:
            p = (p * c.cst) % (1 << node.width)
        res = Const(p, node.width)
    elif op in ('M', 'P'):
        p = 1
        for c in newChildren:
            p = gmulInt(p, c.cst)
        res = Const(p, node.width)
    elif op == '^':
        v = 0
        for c in newChildren:
            v ^= c.cst
        res = Const(v, node.width)
    elif op == '&':
        v = (1 << node.width) - 1
        for c in newChildren:
            v &= c.cst
        res = Const(v, node.width)
    elif op == '|':
        v = 0
        for c in newChildren:
            v |= c.cst
        res = Const(v, node.width)
    elif op == '~':
        v = ((1 << node.width) - 1) ^ newChildren[0].cst
        res = Const(v, node.width)
    else:
        assert False, f"Unsupported op in getExpValue: {op}"

    expCache[node] = res
    return res
