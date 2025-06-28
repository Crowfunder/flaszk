from sympy.core.mod import Mod
from sympy.ntheory.generate import randprime

def generateExponent(p):
    return randprime(1000,p)


def modularExponentation(x,a,p):
    key=pow(x,a)
    return Mod(key,p)