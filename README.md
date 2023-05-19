# VerifMSI: Practical Verification of Masking Schemes Implementations

VerifMSI is a formal verification tool for the probing security of masked implementations. It provides a way for verifying different security properties on a set of symbolic expressions or on a hardware circuit (gadget).

VerifMSI is a python3 library extending [LeakageVerif](https://github.com/quentin-meunier/LeakageVerif). This README file contains common parts with the one of LeakageVerif.

VerifMSI offers a set of constructs and functions for writing and verifying symbolic expressions, at algorithmic or gate level. A symbolic expression in VerifMSI is a fixed width expression comprising operations on constants and symbolic variables. Each symbolic variable has a type between secret, share, mask and public. VerifMSI verifies that the distribution of the expression value is independent from the secret values it contains, considering that mask variables follow an random uniform distribution.

This work has been accepeted at the SECRYPT 2023 conference as a short paper (reference to come), and available as full paper under the following reference:
Q. L. Meunier, A. R. Taleb "VerifMSI: Practical Verification of Masking Schemes Implementation", (complete)
[Link](link)


## Installation

As a python library, VerifMSI just needs to be cloned to a directory called `verif_msi`, which is the name of the python module it provides. The parent directory of `verif_msi` must be added to the PYTHONPATH environment variable. VerifMSI has only be tested on Linux so far.


## Usage

In order to use VerifMSI constructs, put the following line at the beginning of a python file:
```
from verif_msi import *
```

Symbolic variables are created with a function called `symbol`: the first parameter is the symbol name, the second parameter the symbol type ('S' for secret, 'M' for mask and 'P' for a public variable), and the third parameter the symbol width. Constants are created with a function called `constant`, taking as parameters the value and the width.
```
from verif_msi import *

# Creating an 8-bit secret variable named 'k' 
k = symbol('k', 'S', 8)

# Creating an 8-bit mask variable named 'm0'
m = symbol('m', 'M', 8)

# Creating the 8-bit constant 0xAE
c = constant(0xAE, 8)

# Computing an expression
e = k ^ m ^ c

# Checking probing security on e
res = checkTpsVal(e)

if res:
    print('# Expression %s is probing secure' % e)
else:
    print('# Expression %s is not probing secure' % e)

```

VerifMSI also supports hardware constructs (gates and registers) for verifying gadgets implementations. The following code implements the Domain Oriented Masking AND from [1] with two shares. The function `getRealShares` allows to split a secret into a specified number of shares. In this case, the returned elements are symbol typed as shares, such that the linear recombination (xor) of all the shares is the secret. An alternate function, getPseudoShares, allows to make an explicit sharing based on the secret and dedicated masks. The difference in the secret representation (explicit or shares) determines which security properties can be verified.

```
a = symbol('a', 'S', 1) # 1-bit secret named 'a'
b = symbol('b', 'S', 1) # 1-bit secret name 'b'
z10 = symbol('z10', 'M', 1) # 1-bit mask named 'z10'

# Do the sharing for 'a' and 'b'
a0, a1 = getRealShares(a, 2)
b0, b1 = getRealShares(b, 2)

# Create input gates
a0 = inputGate(a0) 
a1 = inputGate(a1)
b0 = inputGate(b0)
b1 = inputGate(b1)
z10 = inputGate(z10)

# Cross products
a0b0 = andGate(a0, b0)
a0b1 = andGate(a0, b1)
a1b0 = andGate(a1, b0)
a1b1 = andGate(a1, b1)

# Remaining gates and registers
a1b0 = xorGate(a1b0, z10)
a1b0 = Register(a1b0)
a0b1 = xorGate(a0b1, z10)
a0b1 = Register(a0b1)
c0 = a0b0
c0 = xorGate(c0, a0b1)
c1 = a1b1
c1 = xorGate(c1, a1b0)

# Check the NI security property
checkSecurity(order, withGlitches, 'ni', c0, c1)
```

The gadget inputs must be defined with the `inputGate` function; the available logic gates are `andGate`, `orGate`, `xorGate` and `notGate`. The `Register`construct allows to stop the propagation of glitches.
The function `checkSecurity` takes as parameters the security order, a boolean indicating if glitches must be considered, the security property (see corresponding section), and a list of wires corresponding to the outputs of the gadget. 


## Security Properties

VerifMSI supports the verification of 5 security properties:
* Threshold Probing Security ('tps') [2], requiring an explicit secret representation;
* Non-Interference ('ni') [3], requiring a share representation;
* Strong Non-Interference ('sni') [3], requiring a share representation;
* Probe Isolating Non-Interference ('pini') [4], requiring a share representation;
* Relaxed Non-Interference ('rni'), requiring a share representation and defined in VerifMSI article.


## Supported operations

* `^`: bitwise exclusive OR
* `&`: bitwise AND
* `|`: bitwise OR
* `~`: bitwise NOT
* `+`: arithmetic addition
* `-`: arithmetic subtraction
* `<<`: logical shift left. The shift amount must be a constant or a python integer, and cannot be symbolic.
* `>>`: arithmetic shift right. The shift amount must be a constant or a python integer, and cannot be symbolic.
* `*`: integer multiplication, modulo 2 to the power of the expression width.
* `**`: integer power, modulo 2 to the power of the expression width.


Some operations are implemented in the form of functions:

* `LShR(x, y)`: logical shift right. The shift amount y must be a constant or a python integer, and cannot be symbolic.
* `RotateRight(x, y)`: right shift with rotation
* `Concat(x, y, ...)`: concatenation of expressions
* `Extract(msb, lsb, e)`: extraction of some of the bits in `e`, from the most significant bit given by msb, to the least significant bit given by lsb.
* `ZeroExt(v, e)`: zero extension: extension of the expression `e` by the addition of v bits with value 0 on the left of `e`
* `SignExt(v, e)`: signed extension: extension of the expression `e` by adding v time the MSB of `e` on its left

Some operations related to Galois Fields are implemented but are still in experimental state:
* `GMul(x, y, ...)`: Finite Field multiplication. Currently, it is only implemented on 8 bits, and with the irreducible polynomial 0x11B.
* `GPow(x, y)`: Finite Field power
* `GLog(x)`: Finite Field logarithm
* `GExp(x)`: Finite Field exponentiation


## Functionalities

### Simplification

VerifMSI implements a wide range of simplifications, taking advantage of operators properties. In order to simplify an expression, simply call the `simplify` function:
```
p0 = symbol('p0', 'P', 8)
p1 = symbol('p1', 'P', 8)
m = symbol('m', 'M', 8)
e = ((p0 ^ m) | (p1 & constant(0, 8))) ^ (m & constant(0xFF, 8) + (p0 ^ p0))
simplifiedExp = simplify(e)
print('simplifiedExp: %s' % simplifiedExp)
```

### Bit decomposition of expressions

VerifMSI can decompose an expression into a concatenation of bit expressions. Although this feature is mostly used in the verification algorithm, it is possible to get the equivalent bit decomposition with the function `getBitDecomposition`. n-bit symbolic variables are decomposed in n 1-bit variables of the same type.
```
k = symbol('k', 'S', 4)
exp = k & constant(0x5, 4)
bitExp = getBitDecomposition(exp)
print('bitExp: %s' % bitExp)
```

### Arrays

Symbolic array accesses can be modeled in VerifMSI expressions. Currently, only some types of arrays are considered, more specifically those in which the corresponding initialization in the non-symbolic implementation is made without using symbolic variables. This means that accessing to an array with expression `e` as index cannot leak more information than e, and prevents for example to have an index `i` such that `array[i] = exp`, where `exp` is a symbolic expression. This is particularly useful for algorithms like the AES in which the SBox can be implemented as an array. In order to create an array, one has to use the `registerArray` function. Parameters are in order:
* Array name,
* Input width (in bits),
* Output width (in bits),
* Array address
* Array size (in bytes)
* Array function
* Array content

The only mandatory parameters are the name, input width and output width.

For example, the SBox from the AES can be implemented as follows:
```
sbox = [ 0x63, 0x7C, ..., 0x16 ]

registerArray('mysbox', 8, 8, None, None, None, sbox)

m = symbol('m', 'M', 8)
sb = getArrayByName('mysbox')

print('sbox[m]: %s' % sb[m])              # displays 'sbox[m]: mysbox[m]'
print('sbox[0]: %s' % sb[constant(0, 8)]) # displays 'sbox[m]: 0x63'
```

It is advised to specify the content of the array upon registration whenever possible, as this allows to evaluate the expression for concrete input values. This is very useful for checking an implementation, as it is sufficient to replace symbolic variables with constants in order to check the correctness of an implementation. This also allows to use the **concrete evaluation** module functions.

Arrays can also be associated to a function, which is used as a substitute for the expression to use. This allows for example to implement multiplication by 2 or 3 in the AES with an array:
```
mul_02 = [ 0x00, 0x02, 0x04, ..., 0xe5 ]

def mul_02_func(mem, e):
    return GMul(constant(2, 8), e)

registerArray('mul_02', 8, 8, None, 256, mul_02_func, mul_02)
```
Note that this is not necessary when implementing the AES directly because in the latter case we can simply replace the array access with the expression `GMul(constant(2, 8), e)` or `GMul(constant(3, 8), e)`.
Examples using a function can be found in the `aes_sm` benchmark.

Finally, arrays can also be associated to a base address and a size. The base address represents its memory implantation and the size the size it occupies in memory. This mechanism is useful when verifying assembly code. Combined with a function, if a memory access to the array (detected with the base address and size) has a symbolic part, this part can be used as the parameter of the function called. This allows for example to transform the expression Sbox'[x ^ m] into Sbox[x] ^ m' in a compiled version of the AES Herbst scheme.

Examples using the address and size parameters can be found in the `arm_asm` benchmark.

 


### Concrete Evaluation

The concrev module provides functions based on concrete evaluation. This comes in two flavours: exhaustive evaluation and random evaluation. Exhaustive evaluation enumerates all possible symbolic variables' values, and random evaluation evaluate the expression for arbitrarily chosen values. The provided functions are:

* `compareExpsWithExev(e0, e1)`: checks that expressions e0 and e1 are equivalent for all possible combinations of inputs
* `compareExpsWithRandev(e0, e1, nbEval)`: checks that expressions `e0` and `e1` provide the same result for nbEval evaluations, in which the value of all symbolic variables is chosen randomly. This is useful when enumeration is not possible.
* `getDistribWithExev(e)`: Computes the distribution of the expression `e` regarding its secret variables. The first returned value is True iff the expression has a uniform distribution, the second returned value is True iff the distribution is independent from the secret variables' values.


### Verification

For gadgets and hardware circuits, the main verification function is `checkSecurity(order, withGlitches, secProp, *outputs)`, with the following meaning:
* order: security order. For a security order equal to `n`, all tuples of size `n` must verify the security property;
* withGlitches: boolean indicating if glitches are propagated through gates;
* secProp: security property to verify, must be one on 'tps', 'ni', 'sni', 'rni', 'pini';
* outputs: lists of wires (gate outputs) corresponding to the outputs of the gadget.

For software implementations, the main verification function, `checkTpsVal(e)` verifies the threshold probing security of the expression `e`. Some other security properties are also considered, and are detailed in [11]:

* `checkTpsTrans(e0, e1)`: verifies that the couple of expression (e0, e1) is probing secure
* `checkTpsTransXor(e0, e1)`: verifies that expression `e0 ^ e1` is probing secure
* `checkTpsTransBit(e0, e1)`: verifies that each couple of expressions of the form (`e0[i]`, `e1[i]`) is probing secure, where `e0[i]` (resp. `e1[i]`) is the expression of the `i`-th bit of `e0` (resp. `e1`)
* `checkTpsTransXorBit(e0, e1)`: verifies that each expression of the form `e0[i] ^ e1[i]` is probing secure



## Benchmarks

The `benchmarks` directory contains benchmarks from the literature implemented in VerifMSI.

The gadgets benchmarks are the following:
* ISW AND: The logical AND masking scheme from [2]
* ISW AND refresh: A combination of the ISW AND with a circular refresh on one of the input from [5]
* DOM AND: The Domain Oriented Masking implementation of the AND gate from [1], resistant to glitches;
* Refresh N log N: The N log N refresh scheme from [6];
* NI Mult and SNI Mult: The NI and SNI multiplication schemes from [7];
* PINI Mult: The PINI multiplication scheme from [8];
* GMS AND: Two implementations of the AND gate using the Generalized Masking Scheme, described in the article, using respectively 3 and 5 shares from [9];
* TI AND: The balanced Threshold Implementation of the AND gate from [10].
For schemes which are generic to the security order, the benchmark file is a generator which creates the benchmark file for the specified order.


VerifMSI also contains software benchmarks taken from [MaskedVerifBench](https://github.com/quentin-meunier/MaskedVerifBench) which are identical to those in LeakageVerif:
* aes\_herbst (from MaskedVerifBench): masked version of the AES following the scheme in [12], comprising the key schedule and ten rounds.
* aes\_sm (from MaskedVerifBench): masked implementation adapted from [13]. It implements the same masking scheme as the one in [12], but with a symbolic Galois field multiplication by constants 2 and 3 in the mix-columns step, and does not mask the key schedule.
* arm\_asm: Arm assembly implementations of AES-Herbst and of the Secmult program. Minimal models for the ISA and the memory are provided, and the leakage model consists in analyzing the result (value) of each instruction which modifies a general purpose register in the processor core.
* secmult (from MaskedVerifBench): secure Galois field multiplication as described in [14].
* secmult\_sm (from MaskedVerifBench): Secmult algorithm with symbolic multiplication.

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)



## References

[1] Groß, H., Mangard, S., & Korak, T. (2017). An efficient side-channel protected AES implementation with arbitrary protection order. In Topics in Cryptology–CT-RSA 2017: The Cryptographers' Track at the RSA Conference 2017, Springer International Publishing.

[2] Ishai, Y., Sahai, A., and Wagner, D. (2003). Private circuits: Securing hardware against probing attacks. In Annual International Cryptology Conference (pp. 463-481). Springer, Berlin, Heidelberg.

[3] Barthe, G., Belaïd, S., Cassiers, G., Fouque, P. A., Grégoire, B., & Standaert, F. X. (2019). maskverif: Automated verification of higher-order masking in presence of physical defaults. In ESORICS 2019: 24th European Symposium on Research in Computer Security (pp. 300-318). Springer International Publishing.

[4] Cassiers, G., & Standaert, F. X. (2020). Trivially and efficiently composing masked gadgets with probe isolating non-interference. IEEE Transactions on Information Forensics and Security, 15, 2542-2555.

[5] De Cnudde, T., Reparaz, O., Bilgin, B., Nikova, S., Nikov, V., & Rijmen, V. (2016). Masking AES with shares in hardware. In Cryptographic Hardware and Embedded Systems (CHES) 2016. Springer Berlin Heidelberg.

[6] Battistello, A., Coron, J. S., Prouff, E., & Zeitoun, R. (2016). Horizontal side-channel attacks and countermeasures on the ISW masking scheme. In Cryptographic Hardware and Embedded Systems (CHES 2016). Springer Berlin Heidelberg.

[7] Bordes, N., & Karpman, P. (2021). Fast verification of masking schemes in characteristic two. 40th Annual International Conference on the Theory and Applications of Cryptographic Techniques, 2021. Springer International Publishing.

[8] Wang, W., Ji, F., Zhang, J., & Yu, Y. (2023). Efficient Private Circuits with Precomputation. IACR Transactions on Cryptographic Hardware and Embedded Systems.

[9] Reparaz, O., Bilgin, B., Nikova, S., Gierlichs, B., & Verbauwhede, I. (2015). Consolidating masking schemes. 35th Annual Cryptology Conference, 2015. Springer Berlin Heidelberg.

[10] Nikova, S., Rechberger, C., & Rijmen, V. (2006). Threshold implementations against side-channel attacks and glitches. In ICICS (Vol. 4307, pp. 529-545).

[11] Meunier, Q. L., El Ouahma, I. B., and Heydemann, K. (2020, September). SELA: a Symbolic Expression Leakage Analyzer. In International Workshop on Security Proofs for Embedded Systems.

[12] Herbst, C., Oswald, E., and Mangard, S. (2006, June). An AES smart card implementation resistant to power analysis attacks. In International conference on applied cryptography and network security (pp. 239-252). Springer, Berlin, Heidelberg.

[13] Yao, Y., Yang, M., Patrick, C., Yuce, B., and Schaumont, P. (2018, April). Fault-assisted side-channel analysis of masked implementations. In 2018 IEEE International Symposium on Hardware Oriented Security and Trust (HOST) (pp. 57-64). IEEE.

[14] Rivain, M., and Prouff, E. (2010, August). Provably secure higher-order masking of AES. In International Workshop on Cryptographic Hardware and Embedded Systems (pp. 413-427). Springer, Berlin, Heidelberg.



