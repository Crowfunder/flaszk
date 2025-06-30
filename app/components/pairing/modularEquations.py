from sympy.core.mod import Mod
from sympy.ntheory.generate import randprime
from sympy import gcd
from .pairingConfig import *

def generateExponent(p,is_key):
    if is_key:
        return randprime(KEY_GENERATING_THRESHOLD,p)
    else:
        a=randprime(PRIME_GENERATING_THRESHOLD,p-1)
        while gcd(a,p-1) != 1:
            a=randprime(PRIME_GENERATING_THRESHOLD,p-1)
        return a
        


def modularExponentation(x,a,p):
    key=pow(x,a)
    return Mod(key,p)

def inverseModular(x,p):
    return pow(x,-1,p)