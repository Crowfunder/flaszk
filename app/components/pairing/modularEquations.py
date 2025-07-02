from sympy.core.mod import Mod
from sympy.ntheory.generate import randprime
from sympy import gcd
from .pairingConfig import *
from random import randint

def generateExponent(p,is_prime):
    if is_prime:
        return randprime(KEY_GENERATING_THRESHOLD,p)
    else:
        a=randint(PRIME_GENERATING_THRESHOLD,PRIME_GENERATING_LIMIT)
        while gcd(a,p-1) != 1:
            a=randint(PRIME_GENERATING_THRESHOLD,PRIME_GENERATING_LIMIT)
        return a
        


def modularExponentation(x,a,p):
    key=pow(x,a)
    return Mod(key,p)

def inverseModular(x,p):
    return pow(x,-1,p-1)