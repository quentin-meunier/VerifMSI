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



def checkPropVal(e, secProp, params):
    timerStart = timeit.default_timer()

    if e.hasWordOp:
        res = False
        usedBitExp = False
        if not e.wordAnalysisHasFailedOnSubExp:
            if secProp == 'tps':
                res = tps(e)
            elif secProp == 'ni':
                res = ni(e, params)
            elif secProp == 'rni':
                res = rni(e, params)
            elif secProp == 'pini':
                res = pini(e, params)
            if not res:
                e.wordAnalysisHasFailedOnSubExp = True

        if not res and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            if secProp == 'tps':
                res = tps(be)
            elif secProp == 'ni':
                res = ni(be, params)
            elif secProp == 'rni':
                res = rni(be, params)
            elif secProp == 'pini':
                res = pini(be, params)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            if secProp == 'tps':
                res = tps(be)
            elif secProp == 'ni':
                res = ni(be, params)
            elif secProp == 'rni':
                res = rni(be, params)
            elif secProp == 'pini':
                res = pini(be, params)
        else:
            usedBitExp = False
            if secProp == 'tps':
                res = tps(e)
            elif secProp == 'ni':
                res = ni(e, params)
            elif secProp == 'rni':
                res = rni(e, params)
            elif secProp == 'pini':
                res = pini(e, params)

    timerEnd = timeit.default_timer()
    time = timerEnd - timerStart
    return res, usedBitExp, time



def checkTpsVal(e):
    return checkPropVal(e, 'tps', None)

def checkNIVal(e, maxShareOcc):
    return checkPropVal(e, 'ni', maxShareOcc)

def checkRNIVal(e, diff):
    return checkPropVal(e, 'rni', diff)

def checkPINIVal(e, params):
    return checkPropVal(e, 'pini', params)



def checkPropTrans(e0, e1, secProp, params):
    tpsTimerStart = timeit.default_timer()

    e = Concat(e0, e1)
    if e.hasWordOp:
        res = False
        usedBitExp = False
        if not (e0.wordAnalysisHasFailedOnSubExp or e1.wordAnalysisHasFailedOnSubExp):
            if secProp == 'tps':
                res = tps(e)
            elif secProp == 'ni':
                res = ni(e, params)
            elif secProp == 'rni':
                res = rni(e, params)
            elif secProp == 'pini':
                res = pini(e, params)
            # FIXME: if only transition and no value, how to make the flag become true? check each exp independently?
            #if not res:
            #    e0.wordAnalysisHasFailedOnSubExp = True
            #    e1.wordAnalysisHasFailedOnSubExp = True


        if not res and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            if secProp == 'tps':
                res = tps(be)
            elif secProp == 'ni':
                res = ni(be, params)
            elif secProp == 'rni':
                res = rni(be, params)
            elif secProp == 'pini':
                res = pini(be, params)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            if secProp == 'tps':
                res = tps(be)
            elif secProp == 'ni':
                res = ni(be, params)
            elif secProp == 'rni':
                res = rni(be, params)
            elif secProp == 'pini':
                res = pini(be, params)
        else:
            usedBitExp = False
            if secProp == 'tps':
                res = tps(e)
            elif secProp == 'ni':
                res = ni(e, params)
            elif secProp == 'rni':
                res = rni(e, params)
            elif secProp == 'pini':
                res = pini(e, params)

    tpsTimerEnd = timeit.default_timer()
    tpsTime = tpsTimerEnd - tpsTimerStart
    return res, usedBitExp, tpsTime




def checkTpsTrans(e0, e1):
    return checkPropTrans(e0, e1, 'tps', None)

def checkNITrans(e0, e1, maxShareOcc):
    return checkPropTrans(e0, e1, 'ni', maxShareOcc)

def checkRNITrans(e0, e1, diff):
    return checkPropTrans(e0, e1, 'rni', diff)

def checkPINITrans(e0, e1, params):
    return checkPropTrans(e0, e1, 'pini', params)



def checkTpsTransBit(e0, e1):
    if bitExpEnable():
        tpsTime = 0

        assert(e0.width == e1.width)

        for b in range(e0.width - 1, -1, -1):
            tpsTimerStart = timeit.default_timer()
            be = Concat(simplifyCore(Extract(b, b, e0), True, True), simplifyCore(Extract(b, b, e1), True, True))

            resTps = tps(be)
            tpsTimerEnd = timeit.default_timer()
            tpsTime += tpsTimerEnd - tpsTimerStart

            if not resTps:
                break

        return resTps, tpsTime
    else:
        return False, 0


def checkTpsTransXor(e0, e1):
    assert(e0.width == e1.width)
    tpsTimerStart = timeit.default_timer()
    e = simplify(e0 ^ e1)

    if e.hasWordOp:
        resTps = False
        usedBitExp = False
        if not (e0.wordAnalysisHasFailedOnSubExp or e1.wordAnalysisHasFailedOnSubExp):
            resTps = tps(e)
            # FIXME: if only transition and no value, how to make the flag become true? check each exp independently?
            #if not resTps:
            #    e0.wordAnalysisHasFailedOnSubExp = True
            #    e1.wordAnalysisHasFailedOnSubExp = True

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
    return resTps, usedBitExp, tpsTime


def checkTpsTransXorBit(e0, e1):
    if bitExpEnable():
        tpsTime = 0

        assert(e0.width == e1.width)

        for b in range(e0.width - 1, -1, -1):
            tpsTimerStart = timeit.default_timer()
            be = simplifyCore(Extract(b, b, e0) ^ Extract(b, b, e1), True, True)

            resTps = tps(be)
            tpsTimerEnd = timeit.default_timer()
            tpsTime += tpsTimerEnd - tpsTimerStart

            if not resTps:
                break

        return resTps, tpsTime
    else:
        return False, 0


