import random
import math

import math
import random
import Crypto.Util.number
import sys 

print("-----------------------------------------")
bits=16
print (" No of bits : ", bits)

#def GenerateRandomPrimeNumbers():
    #while(1):
      #d = 0
      #PrimeNumber = random.randint(32769,65535) 
      #for i in range(1, PrimeNumber):
       #  if (PrimeNumber % i == 0):
       #     d= d+1
      #if (d ==1):
       #  return PrimeNumber

#p = GenerateRandomPrimeNumbers()
#q = GenerateRandomPrimeNumbers()

p=34687
q=38053
print ("\n Random 16-bit Prime Number (p): ",p)


print (" Random 16-bit Prime Number (q): ",q)


N=p*q
print ("\n N = p*q =",N)

PHI = (p-1)*(q-1)
print ("\n ϕ(n) = (p-1)*(q-1) =",PHI)


def GeneratingRandomValueofe(PHI):
  while(1):
      UPHI= round(PHI/2)
      e = random.randint(3, UPHI) 
      e = (e*2) +1
      if (e%2 == 1 and e < PHI):
         x = PHI
         y = e
         while(y):
             x,y = y, x%y
             if(y == 1):
                 return e

e = Crypto.Util.number.getPrime(16, randfunc=Crypto.Random.get_random_bytes)
print("\n value of ϕ(n) :", PHI)
print(" Value of e :", e)

def GeneratingModInverse(e,PHI):
    s=0; old_s=1
    t=1; old_t=0
    r=e; old_r=PHI
    while r!=0:
        q = old_r//r
        old_r,r = r, old_r - (q*r)
        old_s,s = s, old_s - (q*s)
        old_t,t = t, old_t - (q*t)
    if old_t<0:
        old_t+=PHI
    print('\n GCD of e and ϕ(n) : ',old_r)
    print(' d=',old_t)
    return old_t

d= GeneratingModInverse(e,PHI)
print ("\n d = e(inverse) mod ϕ(n) = ",d)

print("-----------------------------------------")

def initEncryption():

     print("Partner's Public Key N:")
     pubKeyN = int(input())
     print("Partner's Public Key e:")
     pubKeye = int(input())
     print("Message to be Encrypted")
     msg = str(input())
     Lst1 = []
     msgs = []
     sb = ''
     for i in range(0, len(msg), 3):
        if (len(msg) - i > 3): 
            substng = msg[i:i+3]
            Lst1.append(substng)
        else:
            substng = msg[i :]
            Lst1.append(substng)
     print(Lst1)
     for x in Lst1:
        messageChunk = Encryption(x, pubKeyN, pubKeye)
        msgs.append(messageChunk)
     for i in msgs:
        sb = sb+str(i)+','
     sb = sb[0:-1]
     print('['+sb+']')

def Encryption(str, N, e):
     sb = ''
     for i in str:
        ascii = ord(i)
        hexString = hex(ascii)
        sb +=hexString.replace('0x','')
     value = int(sb,16)
     enc_message = Squareandmultiply(value, e, N)
     return enc_message

def Squareandmultiply( str,  e,  N):
    Dict = {} 
    binarystring = bin(e).replace("0b", "")
    reverse=binarystring[::-1]
    result = 0
    endresult = 1
    for i in range(len(binarystring)):
        if (i == 0):
            result = str
        else:
            result = result * result
            if (result >= N):
                quo = result // N
                result -= quo * N
        Dict[i] =  result
    for j in range(0, len(reverse)):
        if (reverse[j] == '1'):
            endresult *= Dict[j]
            if (endresult >= N):
                quo = endresult // N
                endresult -= quo * N

    if (endresult >= N):
        quo = endresult // N
        endresult -=quo * N
    return endresult


def initDecryption():
     print("Your Public Key N:")
     pubKeyN = int(input())
     print("Your Private key d:")
     PvtKeyd = int(input())
     print("Message to be Decrypted :")
     msg = str(input())
     msg = msg.replace('[', '')
     msg = msg.replace(']', '')
     msgs = []
     values = msg.split(",")
     for i in values:
        chunk = int(i)
        messageChunk = Decryption(chunk, PvtKeyd, pubKeyN)
        msgs.append(messageChunk)
     print(msgs)
     concat = ''.join(msgs)
     print(concat)

def Decryption(str, D, N):
    sb=''
    decryptedMsg = Squareandmultiply(str, D, N)
    hexString = hex(decryptedMsg)
    sb +=hexString.replace('0x','')
    bytesFormat = bytes.fromhex(sb)
    decrypted_msg = bytesFormat.decode("ASCII")
    return decrypted_msg

def Signature():
     sb =''
     print("Your Public key N")
     pubKeyN = int(input())
     print("Your Private key D")
     PvtKeyd = int(input())
     print("Your Signature to be encrypted")
     msg = str(input())
     Lst1 = []
     msgs=[]
     for i in range(0, len(msg), 3):
        if (len(msg) - i > 3): 
            substng = msg[i:i+3]
            Lst1.append(substng)
        else:
            substng = msg[i :]
            Lst1.append(substng)
     print(Lst1)
     for x in Lst1:
        messageChunk = Encryption(x, pubKeyN, PvtKeyd)
        msgs.append(messageChunk)
     for i in msgs:
        sb = sb+str(i)+','
     sb = sb[0:-1]
     print('Signed Text :')
     print('['+sb+']')

def Verification():
     print("Partner's Public key N")
     pubKeyN = int(input())
     print("Partner's Public key e")
     PvtKeyd = int(input())
     print("Partners sign : ")
     sign = str(input())
     print("Partners Ecrypted Signature : ")
     msg = str(input())
     msg = msg.replace('[', '')
     msg = msg.replace(']', '')
     msgs = []
     values = msg.split(",")
     for i in values:
        chunk = int(i)
        messageChunk = Decryption(chunk, PvtKeyd, pubKeyN)
        msgs.append(messageChunk)
     concat = ''.join(msgs)
     if(sign == concat):
         print('Signature verification is: True')
     else:
         print('Signature verification is: False')
     print(concat)



print('Select: \n 1 Encryption \n 2 Decryption \n 3 Signature \n 4 Verifying Signature')
select = int(input())
if select ==1:
    initEncryption()
if select ==2:
    initDecryption()
if select ==3:
    Signature()
if select ==4:
    Verification()
else:
    print('Select an Option')
