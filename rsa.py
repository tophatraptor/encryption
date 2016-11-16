#!usr/bin/python3
import random
import math
import multiprocessing as mp
import os
import sys
os.system("taskset -p 0xff %d" % os.getpid())

#HELPER FUNCTIONS

def isprime(x):
    if x >= 2:
        a = int(math.ceil(math.sqrt(x)))+1
        for y in range(2,a):
            if not ( x % y ):
                return False
    return True

def genprimes(a,b):
    for i in range(a,b):
        if isprime(i):
            print (i)

def randprime(a,b): #Don't pass in 'b' larger than 10**15 for sub-2-second performance times
    n = random.randint(a,b)
    while not(isprime(n)):
        n=random.randint(a,b)
    return n

def modexp(base,exp,mod): #implementing modular exponentiation w/ binary exponentiation
#O(log(exp))
    if mod==1: return 0
    result=1
    base = base%mod
    while exp>0:
        if (exp%2==1):
            result=(result*base)%mod
        exp=exp >> 1
        base=(base*base)%mod
    return result


def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)

def primecoprime(a):
    n=randprime(19,1000)
    while (gcd(a,n)!=1): #implementing n%a!=1 only returned 3,5, or 13
        n=randprime(2,a)
    return n

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
        (oldr, r) = (r, oldr-quotient*r)
        (olds, s) = (s, olds-quotient*s)
        (oldt, t) = (t, oldt-quotient*t)
    return oldr, olds, oldt

def modmultinv(a, m):
    #An implementation of a multiplicative modular inverse function
    #Uses the output from the extended gcd function listed immediately above
    g, x, y = egcd(a, m)
    if g != 1:
       return None
    else:
       return x % m

def encrypt(message,e,m):
    return (message**e)%m

def decrypt(c,dp,dq,p,q,qinv):
    m1=(c**dp)%p
    m2=(c**dq)%q
    h=(qinv*(m1-m2))%p
    m=m2+h*q
    return m

#MAIN PROGRAM


def genvalues():
    p = randprime(10**3,10**6)
    q = randprime(10**3, 10**6)
    n=p*q
    totient=(p-1)*(q-1)
    t1=(p-1)
    t2=(q-1)
    e=primecoprime(totient)
    d=modmultinv(e,totient)

    return p,q,n,totient,t1,t2,e,d

def RSA(message,p,q,n,totient,t1,t2,e,d):
    mess = [ord(c) for c in message]
    print ("The message in ASCII form:")
    print (mess)
    print ("\n")
    publickey=[n,e]
    print ("The current public key is: {}\n".format(publickey))
    privatekey=d
    print ("The current private key is: {}\n".format(privatekey))
    enc = [encrypt(ord(c),e,n) for c in message]
    #at this point, enc should have a list of encrypted ASCII character values
    print ("The encrypted ASCII values: ")
    print (enc)
    print ("\n")
    dp=d%t1
    dq=d%t2
    qinv=modmultinv(p,q)
    dec=[]
    print ("The decrypted ASCII tableset:")
    cpucount = mp.cpu_count()
    pool = mp.Pool(processes=cpucount)
    dec = [pool.apply(decrypt,args=(c,dp,dq,p,q,qinv,)) for c in enc]
    print (dec)
    print ("\n")
    print ("The decrypted message: ")
    out=[chr(d) for d in dec]
    print (''.join(out))
    print ("\n")

def main():
    print ("To generate a new key, type 'newkey'. To exit, type 'q'\n")
    inputmessage = input('What would you like to encrypt?: ')
    p,q,n,totient,t1,t2,e,d=genvalues()
    RSA(inputmessage,p,q,n,totient,t1,t2,e,d)
    while (True):
        inputmessage = input('Next phrase to encrypt: ')
        if (inputmessage=='newkey'):
            p,q,n,totient,t1,t2,e,d=genvalues()
            inputmessage = input('Next phrase to encrypt: ')
        if (inputmessage=='q'):
            break
        RSA(inputmessage,p,q,n,totient,t1,t2,e,d)


if __name__ == '__main__':
    main()
