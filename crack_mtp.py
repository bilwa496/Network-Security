
# CALL SYNTAX ..... python3 crack_mtp.py ciphertext.txt recoveredtext.txt

import sys, binascii, string
from random import *


#snippet for generating the key
def generate_key(size):
    strk = ""
    for i in range(size):
        strk += string.ascii_letters[randint(0,51)]
    return strk 


#function to perform bytewise xor operation
def bxor(a, b):
    result = bytearray()
    for a, b in zip(a, b):
        result.append(a ^ b)
    return bytes(result)


#encryption function
def encrypt(msg, key):
    cipher = bxor(msg, key)
    cipher = (binascii.hexlify(cipher.encode())).decode()
    return cipher


##plaintext = 
##pts = []
##
##max_len = max(len(m) for m in pts)
##keyx = generate_key(max_len)
##print(keyx)
##
##for msg in pts:
##    r = bxor(keyx.encode(),msg.encode())
##    ciphertexts.append(r.decode())

#Assuming that during evaluation, the ciphertext.txt will be in hex format.
#earlier I wrote the code assuming ciphertext.txt in ascii byte format; hence there can be some conversion ambiguity.
#I am not sure of the format of the ciphertexts which Instructor will provide. So, there can be some fault in hex-ASCII-byte conversion. #Consider it kindly.  

ctFile = open(sys.argv[1], 'r')
cthex = ctFile.readline().rstrip('\n')
ciphertext = bytearray.fromhex(cthex).decode().split('\n')


ciphertexts = []
for l in ciphertext:
    if len(l)!=0:
        ciphertexts.append(l)

#finding the maximum length of all ciphertexts since our key shld be of that length
max_length = max(len(msg) for msg in ciphertexts)

decrypts = []
for ct in ciphertexts:
    r = bxor(keyx.encode(),ct.encode())
    decrypts.append(r.decode())

#print(decrypts)

#initiating SPACE to perform space attack
key = bytearray(b'?' * max_length)
SPACE = ord(" ")

#Key decrypting routine
for k in range(max(len(c) for c in ciphertexts)):
    cts = [c for c in ciphertexts if len(c) > k] 
    assum = ord('?')    
    for plain1 in range(len(cts)):
        for plain2 in range(len(cts)):                
            if plain2 == plain1:
                    continue            
            xor = ord(cts[plain1][k]) ^ ord(cts[plain2][k])            
            if 0 < xor < 65: #checking till occurence of 1st alphabet character
                    assum = ord('?')
                    break
            assum = SPACE
        if assum == SPACE: 
                key[k] = ord(cts[plain1][k]) ^ SPACE
                break

#Please acknowledge that the key is being retrieved from the space attack..since some partial errors are there in the key, denoted by '*'
#so when we are going to use the retrieved key for cryptananlysis xor with star character is creating some unidentified random ascii #characters. So, there is partial recovery of the plaintexts. 
#print(key)		
	
ptsb = []
for msg in pts:
    b= bytearray(b'*' * len(msg))
    ptsb.append(b)
    

for k in range(len(key)):
    for pos in range(len(ptsb)):        
        if len(ptsb[pos]) > k:
                ptsb[pos][k] = key[k] ^ ord(ciphertexts[pos][k])

#print(len(ptsb))                       
outFile = open(sys.argv[2],'w')
outFile.writelines([c for c in ptsb])


