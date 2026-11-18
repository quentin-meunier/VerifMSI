# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

import timeit

from .node import *
from .simplify import *
from .tps import *
from .utils import *


class CheckPropResult(int):
    def __new__(cls, res, usedBitExp=False, time=0.0):
        obj = super().__new__(cls, 1 if res else 0)
        obj.res = bool(res)
        obj.usedBitExp = bool(usedBitExp)
        obj.time = float(time)
        return obj

    def __bool__(self):
        return self.res

    def __iter__(self):
        return iter((self.res, self.usedBitExp, self.time))

    def __getitem__(self, idx):
        return (self.res, self.usedBitExp, self.time)[idx]

    def __len__(self):
        return 3

    def __repr__(self):
        return 'True' if self.res else 'False'


class CheckBitResult(int):
    def __new__(cls, res, time=0.0):
        obj = super().__new__(cls, 1 if res else 0)
        obj.res = bool(res)
        obj.time = float(time)
        return obj

    def __bool__(self):
        return self.res

    def __iter__(self):
        return iter((self.res, self.time))

    def __getitem__(self, idx):
        return (self.res, self.time)[idx]

    def __len__(self):
        return 2

    def __repr__(self):
        return 'True' if self.res else 'False'


def checkPropVal(e, secProp, params, usedBitExpRet=None):
    timerStart = timeit.default_timer()

    def call_prop(target):
        if secProp == 'tps':
            return tps(target)
        elif secProp == 'ni':
            return ni(target, params)
        elif secProp == 'rni':
            return rni(target, params)
        elif secProp == 'pini':
            return pini(target, params[0], params[1])
        elif secProp == 'opini':
            return opini(target, params[0], params[1], params[2])
        assert False

    if e.hasWordOp:
        res = False
        usedBitExp = False
        if not e.wordAnalysisHasFailedOnSubExp:
            res = call_prop(e)
            if not res:
                e.wordAnalysisHasFailedOnSubExp = True

        if not res and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            res = call_prop(be)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            res = call_prop(be)
        else:
            usedBitExp = False
            res = call_prop(e)

    timerEnd = timeit.default_timer()
    time = timerEnd - timerStart
    return CheckPropResult(res, usedBitExp, time)


def checkTpsVal(e, usedBitExpRet=None):
    return checkPropVal(e, 'tps', None, usedBitExpRet)


def checkNIVal(e, maxShareOcc, usedBitExpRet=None):
    return checkPropVal(e, 'ni', maxShareOcc, usedBitExpRet)


def checkRNIVal(e, diff, usedBitExpRet=None):
    return checkPropVal(e, 'rni', diff, usedBitExpRet)


def checkPINIVal(e, maxShareOcc, outputIndexes=None, usedBitExpRet=None):
    if isinstance(maxShareOcc, tuple):
        outputIndexes = maxShareOcc[1]
        maxShareOcc = maxShareOcc[0]
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    return checkPropVal(e, 'pini', (maxShareOcc, outputIndexes), usedBitExpRet)


def checkOPINIVal(e, maxShareOcc, outputIndexes=None, allOutputLeakages=None, usedBitExpRet=None):
    if isinstance(maxShareOcc, tuple):
        outputIndexes = maxShareOcc[1] if len(maxShareOcc) > 1 else None
        allOutputLeakages = maxShareOcc[2] if len(maxShareOcc) > 2 else None
        maxShareOcc = maxShareOcc[0]
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    if allOutputLeakages is None:
        allOutputLeakages = []
    return checkPropVal(e, 'opini', (maxShareOcc, outputIndexes, allOutputLeakages), usedBitExpRet)


def checkTpsValBit(e):
    res = True
    for i in range(e.width):
        b = simplify(Extract(i, i, e), usbv=True)
        res = tps(b)
        if not res:
            break
    return res


def checkNIValBit(e, maxShareOcc):
    res = True
    for i in range(e.width):
        b = simplify(Extract(i, i, e), usbv=True)
        res = ni(b, maxShareOcc)
        if not res:
            break
    return res


def checkRNIValBit(e, diff):
    res = True
    for i in range(e.width):
        b = simplify(Extract(i, i, e), usbv=True)
        res = rni(b, diff)
        if not res:
            break
    return res


def checkPINIValBit(e, maxShareOcc, outputIndexes=None):
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    res = True
    for i in range(e.width):
        b = simplify(Extract(i, i, e), usbv=True)
        res = pini(b, maxShareOcc, outputIndexes)
        if not res:
            break
    return res


def checkOPINIValBit(e, maxShareOcc, outputIndexes=None, allOutputLeakages=None):
    if isinstance(outputIndexes, int):
        outputIndexes = {outputIndexes}
    elif outputIndexes is None:
        outputIndexes = set()
    if allOutputLeakages is None:
        allOutputLeakages = []
    res = True
    for i in range(e.width):
        b = simplify(Extract(i, i, e), usbv=True)
        res = opini(b, maxShareOcc, outputIndexes, allOutputLeakages)
        if not res:
            break
    return res


def checkPropTrans(e0, e1, secProp, params, usedBitExpRet=None):
    tpsTimerStart = timeit.default_timer()

    e = Concat(e0, e1)

    def call_prop(target):
        if secProp == 'tps':
            return tps(target)
        elif secProp == 'ni':
            return ni(target, params)
        elif secProp == 'rni':
            return rni(target, params)
        elif secProp == 'pini':
            return pini(target, params[0], params[1])
        elif secProp == 'opini':
            return opini(target, params[0], params[1], params[2])
        assert False

    if e.hasWordOp:
        res = False
        usedBitExp = False
        if not (e0.wordAnalysisHasFailedOnSubExp or e1.wordAnalysisHasFailedOnSubExp):
            res = call_prop(e)

        if not res and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            res = call_prop(be)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            res = call_prop(be)
        else:
            usedBitExp = False
            res = call_prop(e)

    tpsTimerEnd = timeit.default_timer()
    tpsTime = tpsTimerEnd - tpsTimerStart
    return CheckPropResult(res, usedBitExp, tpsTime)


def checkTpsTrans(e0, e1):
    return checkPropTrans(e0, e1, 'tps', None)


def checkNITrans(e0, e1, maxShareOcc):
    return checkPropTrans(e0, e1, 'ni', maxShareOcc)


def checkRNITrans(e0, e1, diff):
    return checkPropTrans(e0, e1, 'rni', diff)


def checkPINITrans(e0, e1, params):
    if isinstance(params, tuple):
        return checkPropTrans(e0, e1, 'pini', params)
    return checkPropTrans(e0, e1, 'pini', (params, set()))


def checkOPINITrans(e0, e1, params):
    return checkPropTrans(e0, e1, 'opini', params)


def checkTpsTransBit(e0, e1):
    if bitExpEnable():
        tpsTime = 0
        assert e0.width == e1.width
        for b in range(e0.width - 1, -1, -1):
            tpsTimerStart = timeit.default_timer()
            be = Concat(simplify(Extract(b, b, e0), pei=True, usbv=True), simplify(Extract(b, b, e1), pei=True, usbv=True))
            resTps = tps(be)
            tpsTimerEnd = timeit.default_timer()
            tpsTime += tpsTimerEnd - tpsTimerStart
            if not resTps:
                break
        return CheckBitResult(resTps, tpsTime)
    else:
        return CheckBitResult(False, 0)


def checkTpsTransXor(e0, e1):
    assert e0.width == e1.width
    tpsTimerStart = timeit.default_timer()
    e = simplify(e0 ^ e1)

    if e.hasWordOp:
        resTps = False
        usedBitExp = False
        if not (e0.wordAnalysisHasFailedOnSubExp or e1.wordAnalysisHasFailedOnSubExp):
            resTps = tps(e)

        if not resTps and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
        else:
            usedBitExp = False
            resTps = tps(e)

    tpsTimerEnd = timeit.default_timer()
    tpsTime = tpsTimerEnd - tpsTimerStart
    return CheckPropResult(resTps, usedBitExp, tpsTime)


def checkTpsTransXorBit(e0, e1):
    if bitExpEnable():
        tpsTime = 0
        assert e0.width == e1.width
        for b in range(e0.width - 1, -1, -1):
            tpsTimerStart = timeit.default_timer()
            be = simplify(Extract(b, b, e0) ^ Extract(b, b, e1), pei=True, usbv=True)
            resTps = tps(be)
            tpsTimerEnd = timeit.default_timer()
            tpsTime += tpsTimerEnd - tpsTimerStart
            if not resTps:
                break
        return CheckBitResult(resTps, tpsTime)
    else:
        return CheckBitResult(False, 0)
