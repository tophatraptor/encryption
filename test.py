import random
import math
import multiprocessing
from multiprocessing import Pool
def isprime(x):
    if x >= 2:
        a = int(math.ceil(math.sqrt(x)))+1
        for y in xrange(2,a): #xrange lazily evaluates a list, which is good for saving memory when isprime is being passed a very large number
        #iterating over only odd numbers via xrange(1,a,2) makes isprime faster, but for some reason, it makes the randprime take an extraordinarily long time
            if not ( x % y ):
                return False

    return True

def genprimes(a,b):
    for i in range(a,b):
        if isprime(i):
            print(i)

def randprime(a,b): #The upper limit for this, from a performance standpoint, seems to be 10**15 (for sub-2-second runtimes). RSA is not well-known for its speed, so for now this should be an adequate approach.
    n = random.randint(a,b)
    while not(isprime(n)):
        n=random.randint(a,b)
    return n

def modexporig(base,exp,mod):
    if mod==1: return 0
    c=1
    for e in range(1,exp+1):
        c=(c*base) % mod
    return c

def modexp(base,exp,mod):
    if mod==1: return 0
    result=1
    base = base%mod
    while exp>0:
        if (exp%2==1):
            result=(result*base)%mod
        exp=exp >> 1
        base=(base*base)%mod
    return result

#randprime(0,10**15)

def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)

def primecoprime(a):
    n=randprime(2,a)
    while (gcd(a,n)!=1): #implementing n%a!=0 only returned 3,5, or 13
        n=randprime(2,a)
    return n

def modmultinvbad(e,m):
    #brute force approach
    #doesn't work in nearly a fast enough time with this implementation
    for i in xrange(1,m+1):
        if (i*e)%m==1:
            return i
    return 0

def enc(message,e,m):
    return (message**e)%m

def modmultinv(e,m):
    pass


def modinv(a, m): #Code from the same source as seen above
    g, x, y = egcd(a, m)
    if g != 1:
       return None
    else:
       return x % m


def encrypt(message,e,m):
    return (message**e)%m

def egcd(a,b):
    #implemented using Wikipedia's pseudocode for the Extended Euclidean Algorithm
    #Returns gcd & Bezout pair
    s=0
    t=1
    olds=1
    oldt=0
    r=b
    oldr=a
    while r!=0:
        quotient=oldr//r
        print (quotient)
        (oldr, r) = (r, oldr-quotient*r)
        (olds, s) = (s, olds-quotient*s)
        (oldt, t) = (t, oldt-quotient*t)
        print ("{},{},{}".format(oldr,olds,oldt))
    return oldr, olds, oldt

def egcdnew(a,b):
    s=0
    t=1
    olds=1
    oldt=0
    r=b
    oldr=a
    while r!=0:
        quotient=oldr/r


def modmultinv(a, m):
    #An implementation of a multiplicative modular inverse function
    #Uses the output from the extended gcd function listed immediately above
    g, x, y = egcd(a, m)
    if g != 1:
       return None
    else:
       return x % m
def f(x): return x*x
