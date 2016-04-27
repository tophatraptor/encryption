import random
import math

#HELPER FUNCTIONS

def isprime(x):
    if x >= 2:
        a = int(math.ceil(math.sqrt(x)))+1
        for y in xrange(2,a): #xrange lazily evaluates
        #xrange(1,a,2) makes isprime faster, but makes randprimes hang
            if not ( x % y ):
                return False

    return True

def genprimes(a,b):
    for i in range(a,b):
        if isprime(i):
            print i

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
    n=randprime(19,100)
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
        quotient=oldr/r
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

#MAIN PROGRAM

linespace = "\n"


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
    print linespace
    mess = [ord(c) for c in message]
    print "The message in ASCII form:"
    print mess
    print linespace
    publickey=[n,e]
    print "The current public key is: %s" % publickey
    print linespace
    privatekey=d
    print "The current private key is: %s" % privatekey
    print linespace
    enc = [encrypt(ord(c),e,n) for c in message]
    #at this point, enc should have a list of encrypted ASCII character values
    print "The encrypted ASCII values: "
    print enc
    print linespace
    dp=d%t1
    dq=d%t2
    qinv=modmultinv(p,q)
    dec=[]
    print "The decrypted ASCII tableset:"
    for c in enc:
        m1=(c**dp)%p
        m2=(c**dq)%q
        h=(qinv*(m1-m2))%p
        m=m2+h*q
        dec.append(m)
    print dec
    print linespace
    print "The decrypted message: "
    out=[chr(d) for d in dec]
    print ''.join(out)
    print linespace

def main():
    decide=input('Do you want a terminal RSA session (where you can do multiple entries with a single set of generated keys), or a single use session? (type t or s) ')
    p,q,n,totient,t1,t2,e,d=genvalues()
    if decide=="s":
        print linespace
        inputmessage=input('What message would you like to decrypt/encrypt with RSA? ')
        RSA(inputmessage,p,q,n,totient,t1,t2,e,d)
    if decide=="t":
        inputmessage=input('Phrase to encrypt:  (type \'q\' to exit)')
        while inputmessage!="q":
            RSA(inputmessage,p,q,n,totient,t1,t2,e,d)
            inputmessage=input('Next input? ')

if __name__ == '__main__':
    main()
