#!/usr/bin/env python3
# This file was automatically ported from VerifMSI++
from verif_msi import *
import random


# root       root
# ^          m
# /|\   ->
# k m k

k0 = symbol("k0", 'S', 8)
k1 = symbol("k1", 'S', 8)

n = k0 ^ k1 ^ k0

res = k1

checkResults(n, res)

