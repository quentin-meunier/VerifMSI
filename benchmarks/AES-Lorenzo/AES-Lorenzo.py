#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

test_litteral = False
use_tables = True

def sim(e):
    return simplify(e)

nbExps = 0
nbLeak = 0

def checkExpLeakage(e):
    global nbExps
    global nbLeak
    nbExps += 1

    res, wordRes, tpsTime = checkTpsVal(e)
    if not res:
        nbLeak += 1
        print('# Leakage in value for exp num %d: %s' % (nbExps, e))
        #sys.exit(0)


rand_cnt = 0

linear_sbox_t = [
    0,   31,  62,  33,  124, 99,  66,  93,  248, 231, 198, 217, 132, 155, 186,
    165, 241, 238, 207, 208, 141, 146, 179, 172, 9,   22,  55,  40,  117, 106,
    75,  84,  227, 252, 221, 194, 159, 128, 161, 190, 27,  4,   37,  58,  103,
    120, 89,  70,  18,  13,  44,  51,  110, 113, 80,  79,  234, 245, 212, 203,
    150, 137, 168, 183, 199, 216, 249, 230, 187, 164, 133, 154, 63,  32,  1,
    30,  67,  92,  125, 98,  54,  41,  8,   23,  74,  85,  116, 107, 206, 209,
    240, 239, 178, 173, 140, 147, 36,  59,  26,  5,   88,  71,  102, 121, 220,
    195, 226, 253, 160, 191, 158, 129, 213, 202, 235, 244, 169, 182, 151, 136,
    45,  50,  19,  12,  81,  78,  111, 112, 143, 144, 177, 174, 243, 236, 205,
    210, 119, 104, 73,  86,  11,  20,  53,  42,  126, 97,  64,  95,  2,   29,
    60,  35,  134, 153, 184, 167, 250, 229, 196, 219, 108, 115, 82,  77,  16,
    15,  46,  49,  148, 139, 170, 181, 232, 247, 214, 201, 157, 130, 163, 188,
    225, 254, 223, 192, 101, 122, 91,  68,  25,  6,   39,  56,  72,  87,  118,
    105, 52,  43,  10,  21,  176, 175, 142, 145, 204, 211, 242, 237, 185, 166,
    135, 152, 197, 218, 251, 228, 65,  94,  127, 96,  61,  34,  3,   28,  171,
    180, 149, 138, 215, 200, 233, 246, 83,  76,  109, 114, 47,  48,  17,  14,
    90,  69,  100, 123, 38,  57,  24,  7,   162, 189, 156, 131, 222, 193, 224,
    255
]


log_t = [
    511, 0,   25,  1,   50,  2,   26,  198, 75,  199, 27,  104, 51,  238, 223,
    3,   100, 4,   224, 14,  52,  141, 129, 239, 76,  113, 8,   200, 248, 105,
    28,  193, 125, 194, 29,  181, 249, 185, 39,  106, 77,  228, 166, 114, 154,
    201, 9,   120, 101, 47,  138, 5,   33,  15,  225, 36,  18,  240, 130, 69,
    53,  147, 218, 142, 150, 143, 219, 189, 54,  208, 206, 148, 19,  92,  210,
    241, 64,  70,  131, 56,  102, 221, 253, 48,  191, 6,   139, 98,  179, 37,
    226, 152, 34,  136, 145, 16,  126, 110, 72,  195, 163, 182, 30,  66,  58,
    107, 40,  84,  250, 133, 61,  186, 43,  121, 10,  21,  155, 159, 94,  202,
    78,  212, 172, 229, 243, 115, 167, 87,  175, 88,  168, 80,  244, 234, 214,
    116, 79,  174, 233, 213, 231, 230, 173, 232, 44,  215, 117, 122, 235, 22,
    11,  245, 89,  203, 95,  176, 156, 169, 81,  160, 127, 12,  246, 111, 23,
    196, 73,  236, 216, 67,  31,  45,  164, 118, 123, 183, 204, 187, 62,  90,
    251, 96,  177, 134, 59,  82,  161, 108, 170, 85,  41,  157, 151, 178, 135,
    144, 97,  190, 220, 252, 188, 149, 207, 205, 55,  63,  91,  209, 83,  57,
    132, 60,  65,  162, 109, 71,  20,  42,  158, 93,  86,  242, 211, 171, 68,
    17,  146, 217, 35,  32,  46,  137, 180, 124, 184, 38,  119, 153, 227, 165,
    103, 74,  237, 222, 197, 49,  254, 24,  13,  99,  140, 128, 192, 247, 112,
    7
]


log_pow2_t = [
    511, 0,   50,  2,   100, 4,   52,  141, 150, 143, 54,  208, 102, 221, 191,
    6,   200, 8,   193, 28,  104, 27,  3,   223, 152, 226, 16,  145, 241, 210,
    56,  131, 250, 133, 58,  107, 243, 115, 78,  212, 154, 201, 77,  228, 53,
    147, 18,  240, 202, 94,  21,  10,  66,  30,  195, 72,  36,  225, 5,   138,
    106, 39,  181, 29,  45,  31,  183, 123, 108, 161, 157, 41,  38,  184, 165,
    227, 128, 140, 7,   112, 204, 187, 251, 96,  127, 12,  23,  196, 103, 74,
    197, 49,  68,  17,  35,  32,  252, 220, 144, 135, 71,  109, 60,  132, 116,
    214, 80,  168, 245, 11,  122, 117, 86,  242, 20,  42,  55,  63,  188, 149,
    156, 169, 89,  203, 231, 230, 79,  174, 95,  176, 81,  160, 233, 213, 173,
    232, 158, 93,  211, 171, 207, 205, 91,  209, 88,  175, 234, 244, 215, 44,
    22,  235, 178, 151, 190, 97,  57,  83,  162, 65,  254, 24,  237, 222, 46,
    137, 146, 217, 177, 134, 62,  90,  73,  236, 246, 111, 153, 119, 124, 180,
    247, 192, 99,  13,  118, 164, 67,  216, 85,  170, 82,  59,  47,  101, 15,
    33,  194, 125, 185, 249, 121, 43,  159, 155, 110, 126, 182, 163, 166, 114,
    9,   120, 130, 69,  218, 142, 40,  84,  61,  186, 172, 229, 167, 87,  136,
    34,  37,  179, 70,  64,  92,  19,  105, 248, 113, 76,  238, 51,  199, 75,
    206, 148, 219, 189, 139, 98,  253, 48,  26,  198, 25,  1,   129, 239, 224,
    14
]

log_pow4_t = [
    511, 0,   100, 4,   200, 8,   104, 27,  45,  31,  108, 161, 204, 187, 127,
    12,  145, 16,  131, 56,  208, 54,  6,   191, 49,  197, 32,  35,  227, 165,
    112, 7,   245, 11,  116, 214, 231, 230, 156, 169, 53,  147, 154, 201, 106,
    39,  36,  225, 149, 188, 42,  20,  132, 60,  135, 144, 72,  195, 10,  21,
    212, 78,  107, 58,  90,  62,  111, 246, 216, 67,  59,  82,  76,  113, 75,
    199, 1,   25,  14,  224, 153, 119, 247, 192, 254, 24,  46,  137, 206, 148,
    139, 98,  136, 34,  70,  64,  249, 185, 33,  15,  142, 218, 120, 9,   232,
    173, 160, 81,  235, 22,  244, 234, 172, 229, 40,  84,  110, 126, 121, 43,
    57,  83,  178, 151, 207, 205, 158, 93,  190, 97,  162, 65,  211, 171, 91,
    209, 61,  186, 167, 87,  159, 155, 182, 163, 176, 95,  213, 233, 175, 88,
    44,  215, 101, 47,  125, 194, 114, 166, 69,  130, 253, 48,  219, 189, 92,
    19,  37,  179, 99,  13,  124, 180, 146, 217, 237, 222, 51,  238, 248, 105,
    239, 129, 198, 26,  236, 73,  134, 177, 170, 85,  164, 118, 94,  202, 30,
    66,  133, 250, 115, 243, 242, 86,  63,  55,  220, 252, 109, 71,  77,  228,
    18,  240, 5,   138, 181, 29,  80,  168, 122, 117, 89,  203, 79,  174, 17,
    68,  74,  103, 140, 128, 184, 38,  210, 241, 226, 152, 221, 102, 143, 150,
    157, 41,  183, 123, 23,  196, 251, 96,  52,  141, 50,  2,   3,   223, 193,
    28
]

log_pow16_t = [
    511, 0,   145, 16,  35,  32,  161, 108, 180, 124, 177, 134, 51,  238, 253,
    48,  70,  64,  14,  224, 67,  216, 24,  254, 196, 23,  128, 140, 143, 150,
    193, 28,  215, 44,  209, 91,  159, 155, 114, 166, 212, 78,  106, 39,  169,
    156, 144, 135, 86,  242, 168, 80,  18,  240, 30,  66,  33,  15,  40,  84,
    83,  57,  173, 232, 105, 248, 189, 219, 99,  13,  236, 73,  49,  197, 45,
    31,  4,   100, 56,  131, 102, 221, 223, 3,   251, 96,  184, 38,  59,  82,
    46,  137, 34,  136, 25,  1,   231, 230, 132, 60,  58,  107, 225, 36,  163,
    182, 130, 69,  175, 88,  211, 171, 178, 151, 160, 81,  185, 249, 229, 172,
    228, 77,  202, 94,  63,  55,  122, 117, 250, 133, 138, 5,   79,  174, 109,
    71,  244, 234, 158, 93,  126, 110, 218, 142, 194, 125, 87,  167, 190, 97,
    176, 95,  149, 188, 245, 11,  201, 154, 21,  10,  247, 192, 111, 246, 113,
    76,  148, 206, 141, 52,  241, 210, 74,  103, 183, 123, 204, 187, 227, 165,
    191, 6,   27,  104, 179, 37,  26,  198, 170, 85,  146, 217, 121, 43,  120,
    9,   22,  235, 205, 207, 203, 89,  252, 220, 115, 243, 181, 29,  53,  147,
    72,  195, 20,  42,  214, 116, 65,  162, 233, 213, 101, 47,  61,  186, 68,
    17,  41,  157, 50,  2,   226, 152, 75,  199, 139, 98,  119, 153, 62,  90,
    118, 164, 222, 237, 92,  19,  239, 129, 208, 54,  200, 8,   12,  127, 7,
    112
]

exp_t = [
    1,   3,   5,   15,  17,  51,  85,  255, 26,  46,  114, 150, 161, 248, 19,
    53,  95,  225, 56,  72,  216, 115, 149, 164, 247, 2,   6,   10,  30,  34,
    102, 170, 229, 52,  92,  228, 55,  89,  235, 38,  106, 190, 217, 112, 144,
    171, 230, 49,  83,  245, 4,   12,  20,  60,  68,  204, 79,  209, 104, 184,
    211, 110, 178, 205, 76,  212, 103, 169, 224, 59,  77,  215, 98,  166, 241,
    8,   24,  40,  120, 136, 131, 158, 185, 208, 107, 189, 220, 127, 129, 152,
    179, 206, 73,  219, 118, 154, 181, 196, 87,  249, 16,  48,  80,  240, 11,
    29,  39,  105, 187, 214, 97,  163, 254, 25,  43,  125, 135, 146, 173, 236,
    47,  113, 147, 174, 233, 32,  96,  160, 251, 22,  58,  78,  210, 109, 183,
    194, 93,  231, 50,  86,  250, 21,  63,  65,  195, 94,  226, 61,  71,  201,
    64,  192, 91,  237, 44,  116, 156, 191, 218, 117, 159, 186, 213, 100, 172,
    239, 42,  126, 130, 157, 188, 223, 122, 142, 137, 128, 155, 182, 193, 88,
    232, 35,  101, 175, 234, 37,  111, 177, 200, 67,  197, 84,  252, 31,  33,
    99,  165, 244, 7,   9,   27,  45,  119, 153, 176, 203, 70,  202, 69,  207,
    74,  222, 121, 139, 134, 145, 168, 227, 62,  66,  198, 81,  243, 14,  18,
    54,  90,  238, 41,  123, 141, 140, 143, 138, 133, 148, 167, 242, 13,  23,
    57,  75,  221, 124, 132, 151, 162, 253, 28,  36,  108, 180, 199, 82,  246,

    1,   3,   5,   15,  17,  51,  85,  255, 26,  46,  114, 150, 161, 248, 19,
    53,  95,  225, 56,  72,  216, 115, 149, 164, 247, 2,   6,   10,  30,  34,
    102, 170, 229, 52,  92,  228, 55,  89,  235, 38,  106, 190, 217, 112, 144,
    171, 230, 49,  83,  245, 4,   12,  20,  60,  68,  204, 79,  209, 104, 184,
    211, 110, 178, 205, 76,  212, 103, 169, 224, 59,  77,  215, 98,  166, 241,
    8,   24,  40,  120, 136, 131, 158, 185, 208, 107, 189, 220, 127, 129, 152,
    179, 206, 73,  219, 118, 154, 181, 196, 87,  249, 16,  48,  80,  240, 11,
    29,  39,  105, 187, 214, 97,  163, 254, 25,  43,  125, 135, 146, 173, 236,
    47,  113, 147, 174, 233, 32,  96,  160, 251, 22,  58,  78,  210, 109, 183,
    194, 93,  231, 50,  86,  250, 21,  63,  65,  195, 94,  226, 61,  71,  201,
    64,  192, 91,  237, 44,  116, 156, 191, 218, 117, 159, 186, 213, 100, 172,
    239, 42,  126, 130, 157, 188, 223, 122, 142, 137, 128, 155, 182, 193, 88,
    232, 35,  101, 175, 234, 37,  111, 177, 200, 67,  197, 84,  252, 31,  33,
    99,  165, 244, 7,   9,   27,  45,  119, 153, 176, 203, 70,  202, 69,  207,
    74,  222, 121, 139, 134, 145, 168, 227, 62,  66,  198, 81,  243, 14,  18,
    54,  90,  238, 41,  123, 141, 140, 143, 138, 133, 148, 167, 242, 13,  23,
    57,  75,  221, 124, 132, 151, 162, 253, 28,  36,  108, 180, 199, 82,  246,

    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,

    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,

    0, 0, 0, 0
]


rcon = [ 1, 2, 4, 8, 16, 32, 64, 128, 27, 54 ]


def display_vector(v):
    for i in range(16):
        print('%.2x' % int(str(v[i]), 16), end = '')
    print('')



def get_new_random():
    global rand_cnt
    if test_litteral:
        rand_cnt += 1
        return constant(rand_cnt % 256, 8)
    else:
        r = symbol('r_%d' % rand_cnt, 'M', 8)
        rand_cnt += 1
        return r


def mult(a0, a1, b0, b1):
    r01 = get_new_random()
    e = GExp(a0 + b1)
    e = sim(e)
    checkExpLeakage(e)
    r10 = r01 ^ e
    r10 = sim(r10)
    checkExpLeakage(r10)
    e = GExp(a1 + b0)
    e = sim(e)
    checkExpLeakage(e)
    r10 ^= e
    r10 = sim(r10)
    checkExpLeakage(r10)
    e = GExp(a1 + b1)
    e = sim(e)
    checkExpLeakage(e)

    c0 = r10 ^ e
    c0 = sim(c0)
    checkExpLeakage(c0)
    e = GExp(a0 + b0)
    e = sim(e)
    checkExpLeakage(e)
    c1 = r01 ^ e
    c1 = sim(c1)
    checkExpLeakage(c1)

    return c0, c1


def mult_table(a0, a1, b0, b1):
    exp_t = getArrayByName('exp_t')
    r01 = get_new_random()
    e = a0 + b1
    e = sim(e)
    checkExpLeakage(e)
    e = exp_t[e]
    e = sim(e)
    checkExpLeakage(e)
    r10 = r01 ^ e
    r10 = sim(r10)
    checkExpLeakage(r10)
    e = a1 + b0
    e = sim(e)
    checkExpLeakage(e)
    e = exp_t[e]
    e = sim(e)
    checkExpLeakage(e)
    r10 ^= e
    r10 = sim(r10)
    checkExpLeakage(r10)
    e = a1 + b1
    e = sim(e)
    checkExpLeakage(e)
    e = exp_t[e]
    e = sim(e)
    checkExpLeakage(e)

    c0 = r10 ^ e
    c0 = sim(c0)
    checkExpLeakage(c0)
    e = a0 + b0
    e = sim(e)
    checkExpLeakage(e)
    e = exp_t[e]
    e = sim(e)
    checkExpLeakage(e)
    c1 = r01 ^ e
    c1 = sim(c1)
    checkExpLeakage(c1)

    return c0, c1



def exp254(a0, a1):
    r0_2 = GPow(a0, constant(2, 8))
    r0_2 = sim(r0_2)
    checkExpLeakage(r0_2)
    r1_2 = GPow(a1, constant(2, 8))
    r1_2 = sim(r1_2)
    checkExpLeakage(r1_2)

    e0 = GLog(a0)
    e0 = sim(e0)
    checkExpLeakage(e0)
    e1 = GLog(a1)
    e1 = sim(e1)
    checkExpLeakage(e1)
    e2 = GLog(r0_2)
    e2 = sim(e2)
    checkExpLeakage(e2)
    e3 = GLog(r1_2)
    e3 = sim(e3)
    checkExpLeakage(e3)
    r0_3, r1_3 = mult(e0, e1, e2, e3)

    r0_12 = GPow(r0_3, constant(4, 8))
    r0_12 = sim(r0_12)
    checkExpLeakage(r0_12)
    r1_12 = GPow(r1_3, constant(4, 8))
    r1_12 = sim(r1_12)
    checkExpLeakage(r1_12)

    e0 = GLog(r0_3)
    e0 = sim(e0)
    checkExpLeakage(e0)
    e1 = GLog(r1_3)
    e1 = sim(e1)
    checkExpLeakage(e1)
    e2 = GLog(r0_12)
    e2 = sim(e2)
    checkExpLeakage(e2)
    e3 = GLog(r1_12)
    e3 = sim(e3)
    checkExpLeakage(e3)
    r0_15, r1_15 = mult(e0, e1, e2, e3)

    r0_240 = GPow(r0_15, constant(16, 8))
    r0_240 = sim(r0_240)
    checkExpLeakage(r0_240)
    r1_240 = GPow(r1_15, constant(16, 8))
    r1_240 = sim(r1_240)
    checkExpLeakage(r1_240)

    e0 = GLog(r0_240)
    e0 = sim(e0)
    checkExpLeakage(e0)
    e1 = GLog(r1_240)
    e1 = sim(e1)
    checkExpLeakage(e1)
    e2 = GLog(r0_12)
    e2 = sim(e2)
    checkExpLeakage(e2)
    e3 = GLog(r1_12)
    e3 = sim(e3)
    checkExpLeakage(e3)
    r0_252, r1_252 = mult(e0, e1, e2, e3)

    e0 = GLog(r0_252)
    e0 = sim(e0)
    checkExpLeakage(e0)
    e1 = GLog(r1_252)
    e1 = sim(e1)
    checkExpLeakage(e1)
    e2 = GLog(r0_2)
    e2 = sim(e2)
    checkExpLeakage(e2)
    e3 = GLog(r1_2)
    e3 = sim(e3)
    checkExpLeakage(e3)
    r0_254, r1_254 = mult(e0, e1, e2, e3)

    return r0_254, r1_254


def exp254_table(a0, a1):
    log_t = getArrayByName('log_t')
    log_pow2_t = getArrayByName('log_pow2_t')
    log_pow4_t = getArrayByName('log_pow4_t')
    log_pow16_t = getArrayByName('log_pow16_t')

    r0_2 = log_pow2_t[a0]
    r0_2 = sim(r0_2)
    checkExpLeakage(r0_2)
    r1_2 = log_pow2_t[a1]
    r1_2 = sim(r1_2)
    checkExpLeakage(r1_2)
    e0 = log_t[a0]
    e0 = sim(e0)
    checkExpLeakage(e0)
    e1 = log_t[a1]
    e1 = sim(e1)
    checkExpLeakage(e1)
    r0_3, r1_3 = mult_table(e0, e1, r0_2, r1_2)

    r0_12 = log_pow4_t[r0_3]
    r0_12 = sim(r0_12)
    checkExpLeakage(r0_12)
    r1_12 = log_pow4_t[r1_3]
    r1_12 = sim(r1_12)
    checkExpLeakage(r1_12)

    e0 = log_t[r0_3]
    e0 = sim(e0)
    checkExpLeakage(e0)
    e1 = log_t[r1_3]
    e1 = sim(e1)
    checkExpLeakage(e1)
    r0_15, r1_15 = mult_table(e0, e1, r0_12, r1_12)

    r0_240 = log_pow16_t[r0_15]
    r0_240 = sim(r0_240)
    checkExpLeakage(r0_240)
    r1_240 = log_pow16_t[r1_15]
    r1_240 = sim(r1_240)
    checkExpLeakage(r1_240)

    r0_252, r1_252 = mult_table(r0_240, r1_240, r0_12, r1_12)
    e0 = log_t[r0_252]
    e0 = sim(e0)
    checkExpLeakage(e0)
    e1 = log_t[r1_252]
    e1 = sim(e1)
    checkExpLeakage(e1)
    r0_254, r1_254 = mult_table(e0, e1, r0_2, r1_2)

    return r0_254, r1_254



def add_round_key_masked(maksed_state, state_mask, masked_key, key_mask):
    for i in range(16):
        masked_state[i] ^= masked_key[i]
        masked_state[i] = sim(masked_state[i])
        checkExpLeakage(masked_state[i])
        state_mask[i] ^= key_mask[i]
        state_mask[i] = sim(state_mask[i])
        checkExpLeakage(state_mask[i])


def single_sbox_masked(x, m_x):
    if use_tables:
        x, m_x = exp254_table(x, m_x)
    else:
        x, m_x = exp254(x, m_x)
    lst = getArrayByName('linear_sbox_t')
    x = lst[x] ^ constant(0x63, 8)
    x = sim(x)
    checkExpLeakage(x)
    m_x = lst[m_x]
    m_x = sim(m_x)
    checkExpLeakage(m_x)
    return x, m_x


def sbox_masked(masked_state, state_mask):
    for i in range(16):
        masked_state[i], state_mask[i] = single_sbox_masked(masked_state[i], state_mask[i])


def shift_rows(s):
    temp = s[1]
    s[1] = s[5]
    s[5] = s[9]
    s[9] = s[13]
    s[13] = temp

    temp = s[10]
    s[10] = s[2]
    s[2] = temp
    temp = s[14]
    s[14] = s[6]
    s[6] = temp

    temp = s[3]
    s[3] = s[15]
    s[15] = s[11]
    s[11] = s[7]
    s[7] = temp


def shift_rows_masked(masked_state, state_mask):
    shift_rows(masked_state)
    shift_rows(state_mask)


def mix_columns(state):

    def xtime(y):
        r = (y << 1) ^ ((y >> 7) & constant(0x1b, 8))
        r = sim(r)
        return r

    for i in range(0, 16, 4):
        a = state[i]
        b = state[i + 1]
        c = state[i + 2]
        d = state[i + 3]

        e0 = b ^ c
        e0 = sim(e0)
        checkExpLeakage(e0)
        e1 = e0 ^ d
        e1 = sim(e1)
        checkExpLeakage(e1)
        e2 = a ^ b
        e2 = sim(e2)
        checkExpLeakage(e2)
        state[i] = e1 ^ xtime(e2)
        state[i] = sim(state[i])
        checkExpLeakage(state[i])

        e0 = a ^ c
        e0 = sim(e0)
        checkExpLeakage(e0)
        e1 = e0 ^ d
        e1 = sim(e1)
        checkExpLeakage(e1)
        e2 = b ^ c
        e2 = sim(e2)
        checkExpLeakage(e2)
        state[i + 1] = e1 ^ xtime(e2)
        state[i + 1] = sim(state[i + 1])
        checkExpLeakage(state[i + 1])

        e0 = a ^ b
        e0 = sim(e0)
        checkExpLeakage(e0)
        e1 = e0 ^ d
        e1 = sim(e1)
        checkExpLeakage(e1)
        e2 = c ^ d
        e2 = sim(e2)
        checkExpLeakage(e2)
        state[i + 2] = e1 ^ xtime(e2)
        state[i + 2] = sim(state[i + 2])
        checkExpLeakage(state[i + 2])

        e0 = a ^ b
        e0 = sim(e0)
        checkExpLeakage(e0)
        e1 = e0 ^ c
        e1 = sim(e1)
        checkExpLeakage(e1)
        e2 = d ^ a
        e2 = sim(e2)
        checkExpLeakage(e2)
        state[i + 3] = e1 ^ xtime(e2)
        state[i + 3] = sim(state[i + 3])
        checkExpLeakage(state[i + 3])



def mix_columns_masked(masked_state, state_mask):
    mix_columns(masked_state)
    mix_columns(state_mask)


def compute_key_masked(masked_key, key_mask, rcon):
    buf0 = masked_key[13]
    m_buf0 = key_mask[13]
    buf1 = masked_key[14]
    m_buf1 = key_mask[14]
    buf2 = masked_key[15]
    m_buf2 = key_mask[15]
    buf3 = masked_key[12]
    m_buf3 = key_mask[12]

    buf0, m_buf0 = single_sbox_masked(buf0, m_buf0)
    masked_key[0] ^= buf0 ^ constant(rcon, 8)
    masked_key[0] = sim(masked_key[0])
    checkExpLeakage(masked_key[0])
    key_mask[0] ^= m_buf0
    key_mask[0] = sim(key_mask[0])
    checkExpLeakage(key_mask[0])

    buf1, m_buf1 = single_sbox_masked(buf1, m_buf1)
    masked_key[1] ^= buf1
    masked_key[1] = sim(masked_key[1])
    checkExpLeakage(masked_key[1])
    key_mask[1] ^= m_buf1
    key_mask[1] = sim(key_mask[1])
    checkExpLeakage(key_mask[1])

    buf2, m_buf2 = single_sbox_masked(buf2, m_buf2)
    masked_key[2] ^= buf2
    masked_key[2] = sim(masked_key[2])
    checkExpLeakage(masked_key[2])
    key_mask[2] ^= m_buf2
    key_mask[2] = sim(key_mask[2])
    checkExpLeakage(key_mask[2])

    buf3, m_buf3 = single_sbox_masked(buf3, m_buf3)
    masked_key[3] ^= buf3
    masked_key[3] = sim(masked_key[3])
    checkExpLeakage(masked_key[3])
    key_mask[3] ^= m_buf3
    key_mask[3] = sim(key_mask[3])
    checkExpLeakage(key_mask[3])

    for i in range(4, 16):
        masked_key[i] ^= masked_key[i - 4]
        masked_key[i] = sim(masked_key[i])
        checkExpLeakage(masked_key[i])
        key_mask[i] ^= key_mask[i - 4]
        key_mask[i] = sim(key_mask[i])
        checkExpLeakage(key_mask[i])


def init_masked_array(a, masked_a, a_mask):
    for i in range(16):
        a_mask[i] = get_new_random()
        masked_a[i] = a[i] ^ a_mask[i]


def aes_run(masked_state, state_mask, masked_key, key_mask, ct):
    for i in range(9):
        print('# Round %d' % (i + 1))
        add_round_key_masked(masked_state, state_mask, masked_key, key_mask)
        # shiftrows is done before subbytes so that functions that
        # uses field multiplication are closer to each other
        shift_rows_masked(masked_state, state_mask)
        sbox_masked(masked_state, state_mask)
        compute_key_masked(masked_key, key_mask, rcon[i])
        #display_vector([masked_state[j] ^ state_mask[j] for j in range(16)])
        mix_columns_masked(masked_state, state_mask)
    
    print('# Round 10')
    add_round_key_masked(masked_state, state_mask, masked_key, key_mask)
    shift_rows_masked(masked_state, state_mask)
    sbox_masked(masked_state, state_mask)
    compute_key_masked(masked_key, key_mask, rcon[9])
    add_round_key_masked(masked_state, state_mask, masked_key, key_mask)

    for i in range(16):
        ct[i] = masked_state[i] ^ state_mask[i]




def log_func(mem, e):
    return ZeroExt(24, GLog(e))

def log_pow2_func(mem, e):
    return ZeroExt(24, GLog(GPow(e, constant(2, 8))))

def log_pow4_func(mem, e):
    return ZeroExt(24, GLog(GPow(e, constant(4, 8))))

def log_pow16_func(mem, e):
    return ZeroExt(24, GLog(GPow(e, constant(16, 8))))

def exp_func(mem, e):
    return Extract(7, 0, GExp(e))



if __name__ == '__main__':

    registerArray('linear_sbox_t', 8, 8, None, 256, None, linear_sbox_t)
    registerArray('log_t', 8, 32, None, 256, log_func, log_t)
    registerArray('log_pow2_t', 8, 32, None, 256, log_pow2_func, log_pow2_t)
    registerArray('log_pow4_t', 8, 32, None, 256, log_pow4_func, log_pow4_t)
    registerArray('log_pow16_t', 8, 32, None, 256, log_pow16_func, log_pow16_t)
    registerArray('exp_t', 32, 8, None, 1024, exp_func, exp_t)

    if test_litteral:
        pt = {}
        for i in range(16):
            pt[i] = constant(0x00, 8)

        key = {}
        key[0] = constant(0x80, 8)
        for i in range(1, 16):
            key[i] = constant(0x00, 8)

    else:
        pt = {}
        for i in range(16):
            pt[i] = symbol('pt%.2d' % i, 'P', 8)

        key = {}
        for i in range(16):
            key[i] = symbol('k%.2d' % i, 'S', 8)


    if test_litteral:
        print("Plain text:    ", end = '')
        display_vector(pt)

        print("Key:           ", end = '')
        display_vector(key)

    masked_key = {}
    key_mask = {}
    masked_state = {}
    state_mask = {}
    ct = {}

    init_masked_array(key, masked_key, key_mask)
    init_masked_array(pt, masked_state, state_mask)

    aes_run(masked_state, state_mask, masked_key, key_mask, ct)

    if test_litteral:
        print('Cyphered text (Masked AES): ', end = '')
        display_vector(ct)



