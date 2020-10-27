#Call syntax  python3 crack_classical.py ciphertext.txt recoveredtext.txt

import sys
import collections

from BitVector import *                                                       #(A)

if len(sys.argv) is not 3:                                                    #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the message file and the other for the '''
             '''encrypted output file''')
PassPhrase = "I want to learn cryptograph and network security"                            #(C)

BLOCKSIZE = 64                                                                #(D)
numbytes = BLOCKSIZE // 8                                                     #(E)

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                    #(F)
for i in range(0,len(PassPhrase) // numbytes):                                #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                           #(H)
    bv_iv ^= BitVector( textstring = textstr )

#read the file and ignore all the new line characters

inFile = open(sys.argv[1],'r')
cipherbin = BitVector(hexstring = inFile.readline().rstrip('\n'))

#implementing the Blocks
cipherBlockList = [BitVector(bitstring = cipherbin[i : i+BLOCKSIZE])
                   for i in range(0, len(cipherbin), BLOCKSIZE)]


cipherBlockList.insert(0, bv_iv)

#Blockwise XOR operation
plainXorKey = [cipherBlockList[i]^cipherBlockList[i-1]
               for  i in range(len(cipherBlockList)-1,0,-1)]

plainXorKey = plainXorKey[::-1]

#using the cryptanalysis of the Modified Vigenere Cipher Attack

NUM_ROW = BLOCKSIZE // 8

VigTab = [[] for i in range(NUM_ROW)]

for i in range(len(plainXorKey)):
    pxkStr = str(plainXorKey[i])
    for j in range(0, len(pxkStr), numbytes):
        VigTab[j//8].append(pxkStr[j : j+numbytes])


Key = ""

#we Assume that space ["" Iin ASCII or 0x20 IN HEXADECIMAL] is max frequency string from statistical analysis


def MostFreq(vgRow):
    counter=collections.Counter(vgRow)
    freqDict = dict(counter)
    return max(freqDict, key=freqDict.get)
 

for i in range(NUM_ROW):
    pxkFreq = MostFreq(VigTab[i])
    xorval = int(pxkFreq, 2)^int('00100000',2)
    t_key = bin(xorval)[2:].zfill(len(pxkFreq))
    Key += t_key


#=======================================================================================

#final step of decryption with key being generated from chosen plaintext attack

key_bv = BitVector(bitstring = Key)    

msg_decrypted_bv = BitVector( size = 0 )           

FILEIN = open("ciphertext.txt")                                   
encrypted = BitVector( hexstring = FILEIN.read().rstrip("\n") )
#print(len(encrypted))

# Carry out differential XORing of bit blocks and decryption:
previous_block = bv_iv                                
for i in range(0, len(cipher) // BLOCKSIZE):              
    bv = cipher[i*BLOCKSIZE:(i+1)*BLOCKSIZE]              
    foo = bv.deep_copy()                                       
    bv ^=  previous_block                           
    previous_block = foo                            
    bv ^=  key_bv                                               
    msg_decrypted_bv += bv                       
                                  


output_plaintext = msg_decrypted_bv.getTextFromBitVector()          


# Write the plaintext to the output file:
FILEOUT = open("output.txt", 'w')                               
FILEOUT.write(output_plaintext)                                      
FILEOUT.close()  
