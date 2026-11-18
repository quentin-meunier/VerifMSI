# Copyright (C) 2023, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

import sys

DELETE_NODES = 1
KEEP_NODES = 2
MEMORY_STRATEGY = KEEP_NODES

PROPAGATE_CST_ON_BUILD = True
SIMPLIFY_EXTRACT_ON_BUILD = True
BIT_EXP_ENABLE = True
EXTENDED_SIMPLIFY = True
BIT_SIMPLIFY_PLUS = False
EXTENDED_MERGE_CONCAT = True
SEL_MSK_W_NON_MSKNG_OCC = True
VERIF_REMOVE_CST_IN_ADD = True
REM_SINGLE_INPUT_PROBES = True
REM_REDUNDANT_PROBES = False
BARTHE_OPT = False


# Security Properties
TPS = 'tps'
NI = 'ni'
SNI = 'sni'
RNI = 'rni'
PINI = 'pini'
OPINI = 'opini'


# Backward compatibility aliases
propagateCst = PROPAGATE_CST_ON_BUILD
bitExp = BIT_EXP_ENABLE


def propagateCstOnBuild():
    return PROPAGATE_CST_ON_BUILD

def setPropagateCstOnBuild(val):
    assert isinstance(val, bool)
    global PROPAGATE_CST_ON_BUILD, propagateCst
    PROPAGATE_CST_ON_BUILD = val
    propagateCst = val


def simplifyExtractOnBuild():
    return SIMPLIFY_EXTRACT_ON_BUILD

def setSimplifyExtractOnBuild(val):
    assert isinstance(val, bool)
    global SIMPLIFY_EXTRACT_ON_BUILD
    SIMPLIFY_EXTRACT_ON_BUILD = val


def bitExpEnable():
    return BIT_EXP_ENABLE

def setBitExpEnable(val):
    assert isinstance(val, bool)
    global BIT_EXP_ENABLE, bitExp
    BIT_EXP_ENABLE = val
    bitExp = val


def extendedSimplifyEnable():
    return EXTENDED_SIMPLIFY

def setExtendedSimplifyEnable(val):
    assert isinstance(val, bool)
    global EXTENDED_SIMPLIFY
    EXTENDED_SIMPLIFY = val


def bitSimplifyPlusEnable():
    return BIT_SIMPLIFY_PLUS

def setBitSimplifyPlusEnable(val):
    assert isinstance(val, bool)
    global BIT_SIMPLIFY_PLUS
    BIT_SIMPLIFY_PLUS = val


def extendedMergeConcatEnable():
    return EXTENDED_MERGE_CONCAT

def setExtendedMergeConcatEnable(val):
    assert isinstance(val, bool)
    global EXTENDED_MERGE_CONCAT
    EXTENDED_MERGE_CONCAT = val


def selMskWNonMskngOccEnable():
    return SEL_MSK_W_NON_MSKNG_OCC

def setSelMskWNonMskngOccEnable(val):
    assert isinstance(val, bool)
    global SEL_MSK_W_NON_MSKNG_OCC
    SEL_MSK_W_NON_MSKNG_OCC = val


def verifRemoveCstInAddEnable():
    return VERIF_REMOVE_CST_IN_ADD

def setVerifRemoveCstInAddEnable(val):
    assert isinstance(val, bool)
    global VERIF_REMOVE_CST_IN_ADD
    VERIF_REMOVE_CST_IN_ADD = val


def remSingleInputProbesEnable():
    return REM_SINGLE_INPUT_PROBES

def setRemSingleInputProbesEnable(val):
    assert isinstance(val, bool)
    global REM_SINGLE_INPUT_PROBES
    REM_SINGLE_INPUT_PROBES = val


def remRedundantProbesEnable():
    return REM_REDUNDANT_PROBES

def setRemRedundantProbesEnable(val):
    assert isinstance(val, bool)
    global REM_REDUNDANT_PROBES
    REM_REDUNDANT_PROBES = val


def bartheOptEnable():
    return BARTHE_OPT

def setBartheOptEnable(val):
    assert isinstance(val, bool)
    global BARTHE_OPT
    BARTHE_OPT = val


def dumpConfig(out=sys.stdout):
    out.write("### VerifMSI configuration ###\n")
    out.write("# Compilation flags:\n")
    out.write(f"# MEMORY_STRATEGY: {'KEEP_NODES' if MEMORY_STRATEGY == KEEP_NODES else 'DELETE_NODES'}\n")
    out.write(f"# PROPAGATE_CST_ON_BUILD: {PROPAGATE_CST_ON_BUILD}\n")
    out.write(f"# SIMPLIFY_EXTRACT_ON_BUILD: {SIMPLIFY_EXTRACT_ON_BUILD}\n")
    out.write(f"# BIT_EXP_ENABLE: {BIT_EXP_ENABLE}\n")
    out.write(f"# EXTENDED_SIMPLIFY: {EXTENDED_SIMPLIFY}\n")
    out.write(f"# BIT_SIMPLIFY_PLUS: {BIT_SIMPLIFY_PLUS}\n")
    out.write(f"# EXTENDED_MERGE_CONCAT: {EXTENDED_MERGE_CONCAT}\n")
    out.write(f"# SEL_MSK_W_NON_MSKNG_OCC: {SEL_MSK_W_NON_MSKNG_OCC}\n")
    out.write(f"# VERIF_REMOVE_CST_IN_ADD: {VERIF_REMOVE_CST_IN_ADD}\n")
    out.write(f"# REM_SINGLE_INPUT_PROBES: {REM_SINGLE_INPUT_PROBES}\n")
    out.write(f"# REM_REDUNDANT_PROBES: {REM_REDUNDANT_PROBES}\n")
    out.write(f"# BARTHE_OPT: {BARTHE_OPT}\n")
    out.write("### End of VerifMSI configuration ###\n")
