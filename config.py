# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

import sys


propagateCst = True
bitExp = True


def propagateCstOnBuild():
    return propagateCst

def bitExpEnable():
    return bitExp


def setPropagateCstOnBuild(val):
    assert(isinstance(val, bool))
    global propagateCst
    propagateCst = val

def setBitExpEnable(val):
    assert(isinstance(val, bool))
    global bitExp
    bitExp = val


