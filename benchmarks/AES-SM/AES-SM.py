# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the Muse project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function

from verif_msi import *

testLitteral = False

def sim(e):
    return simplify(e)

nbExps = 0
nbLeak = 0

def checkExpLeakage(e):
    global nbExps
    global nbLeak
    nbExps += 1

    res, wordRes, niTime = checkTpsVal(e)
    if not res:
        nbLeak += 1
        print('# Leakage in value for exp num %d: %s' % (nbExps, e))


sbox = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

mul_02 = [
    0x00, 0x02, 0x04, 0x06, 0x08, 0x0a, 0x0c, 0x0e, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e,
    0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e,
    0x40, 0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e,
    0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7a, 0x7c, 0x7e,
    0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e, 0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e,
    0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa, 0xac, 0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe,
    0xc0, 0xc2, 0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0xd4, 0xd6, 0xd8, 0xda, 0xdc, 0xde,
    0xe0, 0xe2, 0xe4, 0xe6, 0xe8, 0xea, 0xec, 0xee, 0xf0, 0xf2, 0xf4, 0xf6, 0xf8, 0xfa, 0xfc, 0xfe,
    0x1b, 0x19, 0x1f, 0x1d, 0x13, 0x11, 0x17, 0x15, 0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05,
    0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35, 0x2b, 0x29, 0x2f, 0x2d, 0x23, 0x21, 0x27, 0x25,
    0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55, 0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45,
    0x7b, 0x79, 0x7f, 0x7d, 0x73, 0x71, 0x77, 0x75, 0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65,
    0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95, 0x8b, 0x89, 0x8f, 0x8d, 0x83, 0x81, 0x87, 0x85,
    0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5, 0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5,
    0xdb, 0xd9, 0xdf, 0xdd, 0xd3, 0xd1, 0xd7, 0xd5, 0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5,
    0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5, 0xeb, 0xe9, 0xef, 0xed, 0xe3, 0xe1, 0xe7, 0xe5
]


mul_03 = [
    0x00, 0x03, 0x06, 0x05, 0x0c, 0x0f, 0x0a, 0x09, 0x18, 0x1b, 0x1e, 0x1d, 0x14, 0x17, 0x12, 0x11,
    0x30, 0x33, 0x36, 0x35, 0x3c, 0x3f, 0x3a, 0x39, 0x28, 0x2b, 0x2e, 0x2d, 0x24, 0x27, 0x22, 0x21,
    0x60, 0x63, 0x66, 0x65, 0x6c, 0x6f, 0x6a, 0x69, 0x78, 0x7b, 0x7e, 0x7d, 0x74, 0x77, 0x72, 0x71,
    0x50, 0x53, 0x56, 0x55, 0x5c, 0x5f, 0x5a, 0x59, 0x48, 0x4b, 0x4e, 0x4d, 0x44, 0x47, 0x42, 0x41,
    0xc0, 0xc3, 0xc6, 0xc5, 0xcc, 0xcf, 0xca, 0xc9, 0xd8, 0xdb, 0xde, 0xdd, 0xd4, 0xd7, 0xd2, 0xd1,
    0xf0, 0xf3, 0xf6, 0xf5, 0xfc, 0xff, 0xfa, 0xf9, 0xe8, 0xeb, 0xee, 0xed, 0xe4, 0xe7, 0xe2, 0xe1,
    0xa0, 0xa3, 0xa6, 0xa5, 0xac, 0xaf, 0xaa, 0xa9, 0xb8, 0xbb, 0xbe, 0xbd, 0xb4, 0xb7, 0xb2, 0xb1,
    0x90, 0x93, 0x96, 0x95, 0x9c, 0x9f, 0x9a, 0x99, 0x88, 0x8b, 0x8e, 0x8d, 0x84, 0x87, 0x82, 0x81,
    0x9b, 0x98, 0x9d, 0x9e, 0x97, 0x94, 0x91, 0x92, 0x83, 0x80, 0x85, 0x86, 0x8f, 0x8c, 0x89, 0x8a,
    0xab, 0xa8, 0xad, 0xae, 0xa7, 0xa4, 0xa1, 0xa2, 0xb3, 0xb0, 0xb5, 0xb6, 0xbf, 0xbc, 0xb9, 0xba,
    0xfb, 0xf8, 0xfd, 0xfe, 0xf7, 0xf4, 0xf1, 0xf2, 0xe3, 0xe0, 0xe5, 0xe6, 0xef, 0xec, 0xe9, 0xea,
    0xcb, 0xc8, 0xcd, 0xce, 0xc7, 0xc4, 0xc1, 0xc2, 0xd3, 0xd0, 0xd5, 0xd6, 0xdf, 0xdc, 0xd9, 0xda,
    0x5b, 0x58, 0x5d, 0x5e, 0x57, 0x54, 0x51, 0x52, 0x43, 0x40, 0x45, 0x46, 0x4f, 0x4c, 0x49, 0x4a,
    0x6b, 0x68, 0x6d, 0x6e, 0x67, 0x64, 0x61, 0x62, 0x73, 0x70, 0x75, 0x76, 0x7f, 0x7c, 0x79, 0x7a,
    0x3b, 0x38, 0x3d, 0x3e, 0x37, 0x34, 0x31, 0x32, 0x23, 0x20, 0x25, 0x26, 0x2f, 0x2c, 0x29, 0x2a,
    0x0b, 0x08, 0x0d, 0x0e, 0x07, 0x04, 0x01, 0x02, 0x13, 0x10, 0x15, 0x16, 0x1f, 0x1c, 0x19, 0x1a
]



rcon = [ 1, 2, 4, 8, 16, 32, 64, 128, 27, 54 ]
memory = {}


def display_vector(v):
    for i in range(16):
        print('%s ' % v[i], end = '')
    print('')



def shift_rows(state):
    temp = state[1]
    state[1] = state[5]
    state[5] = state[9]
    state[9] = state[13]
    state[13] = temp

    temp = state[10]
    state[10] =state[2]
    state[2]  = temp
    temp = state[14]
    state[14] = state[6]
    state[6] = temp

    temp = state[3]
    state[3] = state[15]
    state[15] = state[11]
    state[11] = state[7]
    state[7] = temp



def mix_columns(state):
    temp = {}
    mul_02_t = getArrayByName('mul_02')
    mul_03_t = getArrayByName('mul_03')

    for i in range(0, 16, 4):
        temp[0] = state[i]
        temp[1] = state[i + 1]
        temp[2] = state[i + 2]
        temp[3] = state[i + 3]

        # state[i]     = mul_2(temp[0]) ^ mul_3(temp[1]) ^       temp[2]  ^       temp[3]
        e = mul_02_t[temp[0]] ^ mul_03_t[temp[1]]
        e = sim(e)
        checkExpLeakage(e)
        e = sim(e ^ temp[2])
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ temp[3]
        e = sim(e)
        checkExpLeakage(e)
        state[i] = e

        # state[i + 1] =       temp[0]  ^ mul_2(temp[1]) ^ mul_3(temp[2]) ^       temp[3]
        e = temp[0] ^ mul_02_t[temp[1]]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ mul_03_t[temp[2]]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ temp[3]
        e = sim(e)
        checkExpLeakage(e)
        state[i + 1] = e

        # state[i + 2] =       temp[0]  ^       temp[1]  ^ mul_2(temp[2]) ^ mul_3(temp[3])
        e = temp[0] ^ temp[1]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ mul_02_t[temp[2]]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ mul_03_t[temp[3]]
        e = sim(e)
        checkExpLeakage(e)
        state[i + 2] = e

        # state[i + 3] = mul_3(temp[0]) ^       temp[1]  ^       temp[2]  ^ mul_2(temp[3])
        e = mul_03_t[temp[0]] ^ temp[1]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ temp[2]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ mul_02_t[temp[3]]
        e = sim(e)
        checkExpLeakage(e)
        state[i + 3] = e


def add_masked_round_key(state, rnd, masked_round_key):
    for i in range(16):
        # state[i] ^= masked_round_key[rnd][i]
        e = state[i] ^ masked_round_key[rnd][i]
        e = sim(e)
        checkExpLeakage(e)
        state[i] = e


def add_masked_round_key_no_verif(state, rnd, masked_round_key):
    for i in range(16):
        # state[i] ^= masked_round_key[rnd][i]
        e = state[i] ^ masked_round_key[rnd][i]
        e = sim(e)
        state[i] = e


def masked_subbyte(state, mask):
    sboxp_t = getArrayByName('sboxp')
    for i in range(16):
        # state[i] = sboxp(state[i], mask)
        e = sboxp_t[state[i]]
        e = sim(e)
        checkExpLeakage(e)
        state[i] = e


def remask(s, m1, m2, m3, m4, m5, m6, m7, m8):
    for i in range(4):
        # s[i * 4]     = s[i * 4] ^ (m1 ^ m5)
        e = m1 ^ m5
        e = sim(e)
        checkExpLeakage(e)
        e = s[i * 4] ^ e
        e = sim(e)
        checkExpLeakage(e)
        s[i * 4] = e

        # s[i * 4 + 1] = s[i * 4 + 1] ^ (m2 ^ m6)
        e = m2 ^ m6
        e = sim(e)
        checkExpLeakage(e)
        e = s[i * 4 + 1] ^ e
        e = sim(e)
        checkExpLeakage(e)
        s[i * 4 + 1] = e

        # s[i * 4 + 2] = s[i * 4 + 2] ^ (m3 ^ m7)
        e = m3 ^ m7
        e = sim(e)
        checkExpLeakage(e)
        e = s[i * 4 + 2] ^ e
        e = sim(e)
        checkExpLeakage(e)
        s[i * 4 + 2] = e

        # s[i * 4 + 3] = s[i * 4 + 3] ^ (m4 ^ m8)
        e = m4 ^ m8
        e = sim(e)
        checkExpLeakage(e)
        e = s[i * 4 + 3] ^ e
        e = sim(e)
        checkExpLeakage(e)
        s[i * 4 + 3] = e



def calc_mixcol_mask(mask):
    mul_02_t = getArrayByName('mul_02')
    mul_03_t = getArrayByName('mul_03')

    mask[6] =  mul_02_t[mask[0]] ^ mul_03_t[mask[1]] ^ mask[2] ^ mask[3]
    mask[7] =  mask[0] ^ mul_02_t[mask[1]] ^ mul_03_t[mask[2]] ^ mask[3]
    mask[8] =  mask[0] ^ mask[1] ^ mul_02_t[mask[2]] ^ mul_03_t[mask[3]]
    mask[9] =  mul_03_t[mask[0]] ^ mask[1] ^ mask[2] ^ mul_02_t[mask[3]]


# Masked Key generation
def key_schedule(key, round_key):
    for i in range(4):
        round_key[i * 4]     = key[i * 4]
        round_key[i * 4 + 1] = key[i * 4 + 1]
        round_key[i * 4 + 2] = key[i * 4 + 2]
        round_key[i * 4 + 3] = key[i * 4 + 3]

    for i in range(4, 44):
        # 44 because there are 11 round keys (176 bytes), and
        # each iteration creates a 1/4th of a round key of 128 bits,
        # i.e. 4 bytes.
        temp = {}
        for j in range(4):
            temp[j] = round_key[(i - 1) * 4 + j]
        if i % 4 == 0:
            k = temp[0]
            temp[0] = temp[1]
            temp[1] = temp[2]
            temp[2] = temp[3]
            temp[3] = k

            sbox_t = getArrayByName('sbox')
            temp[0] = sbox_t[temp[0]]
            temp[1] = sbox_t[temp[1]]
            temp[2] = sbox_t[temp[2]]
            temp[3] = sbox_t[temp[3]]

            temp[0] = temp[0] ^ constant(rcon[int(i / 4) - 1], 8)
        
        round_key[i * 4 + 0] = round_key[(i - 4) * 4 + 0] ^ temp[0]
        round_key[i * 4 + 1] = round_key[(i - 4) * 4 + 1] ^ temp[1]
        round_key[i * 4 + 2] = round_key[(i - 4) * 4 + 2] ^ temp[2]
        round_key[i * 4 + 3] = round_key[(i - 4) * 4 + 3] ^ temp[3]



def init_masked_round_keys(masked_round_key, mask):
    z = constant(0, 8)
    for i in range(10):
        remask(masked_round_key[i], mask[6], mask[7], mask[8], mask[9], mask[4], mask[4], mask[4], mask[4])
    remask(masked_round_key[10], mask[5], mask[5], mask[5], mask[5], z, z, z, z)


def copy_key(masked_round_key, round_key):
    for i in range(11):
        masked_round_key[i] = {}
        for j in range(16):
            masked_round_key[i][j] = round_key[i * 16 + j]



def SBox(e):
    if isinstance(e, ConstNode):
        return Const(sbox[e.cst], 8)

    a = getArrayByName('sbox')
    return a[e]


def sboxp_func(mem, e):
    mask = memory['mask']
    m4 = mask[4]
    m5 = mask[5]
    sbox_t = getArrayByName('sbox')
    return sbox_t[e ^ m4] ^ m5


def mul_02_func(mem, e):
    n = GMul(constant(2, 8), e)
    return n

def mul_03_func(mem, e):
    n = GMul(constant(3, 8), e)
    return n



def simplify_state(x):
    for i in range(16):
        x[i] = sim(x[i])


def masked_aes(key, pt, ct, mask):

    round_key = {}
    masked_round_key = {}
    masked_sbox = {}

    key_schedule(key, round_key)
    copy_key(masked_round_key, round_key)
    calc_mixcol_mask(mask)
    init_masked_round_keys(masked_round_key, mask)
    print('# End of key schedule')

    x = {}
    for i in range(16):
        x[i] = pt[i]

    z = constant(0, 8)
    remask(x, z, z, z, z, mask[6], mask[7], mask[8], mask[9])

   
    ### START analysis ###

    # Rounds
    add_masked_round_key(x, 0, masked_round_key)
    for rnd in range(1, 10):
        print('# Round %d' % rnd)
        simplify_state(x)

        masked_subbyte(x, mask)
        shift_rows(x)
        remask(x, mask[5], mask[5], mask[5], mask[5], mask[0], mask[1], mask[2], mask[3])
        mix_columns(x)
        add_masked_round_key(x, rnd, masked_round_key)

    print('# Round 10')
    masked_subbyte(x, mask)
    shift_rows(x)
    ### End analysis ###
    add_masked_round_key_no_verif(x, 10, masked_round_key)

    simplify_state(x)
    print('# End of AES')
    print('# Total Nb. of expression analysed: %d' % nbExps)
    print('# Total Nb. of expression leaking: %d' % nbLeak)
    # Writing output ciphered text
    for i in range(16):
        ct[i] = x[i]


if __name__ == '__main__':

    registerArray('sbox', 8, 8, None, 256, None, sbox)
    registerArray('sboxp', 8, 8, None, 256, sboxp_func, None)
    registerArray('mul_02', 8, 8, None, 256, mul_02_func, mul_02)
    registerArray('mul_03', 8, 8, None, 256, mul_03_func, mul_03)

    mask = {}

    if testLitteral:
        pt = {}
        for i in range(16):
            pt[i] = constant(0x00, 8)

        key = {}
        key[0] = constant(0x80, 8)
        for i in range(1, 16):
            key[i] = constant(0x00, 8)

        mask[0] = constant(0xFA, 8)
        mask[1] = constant(0x7C, 8)
        mask[2] = constant(0x7E, 8)
        mask[3] = constant(0x38, 8)
        mask[4] = constant(0xD6, 8)
        mask[5] = constant(0x94, 8)

    else:
        pt = {}
        for i in range(16):
            pt[i] = symbol('pt%.2d' % i, 'P', 8)

        key = {}
        for i in range(0, 16):
            key[i] = symbol('k%.2d' % i, 'S', 8)

        for i in range(6):
            mask[i] = symbol('m%d' % i, 'M', 8)


    if testLitteral:
        print("Plain text:    ", end = '')
        display_vector(pt)

        print("Key:           ", end = '')
        display_vector(key)

    memory['mask'] = mask
    ct = {}
    masked_aes(key, pt, ct, mask)

    if testLitteral:
        print('Cyphered text (Masked AES): ', end = '')
        display_vector(ct)

