#!/usr/bin/env python


###  Call syntax:

###

###  python3 decrypt_classical.py ciphertext.txt output.txt

###

###  The decrypted output is deposited in the file 'output.txt'


import sys
from BitVector import *                                         


if len(sys.argv) is not 3:                                     
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')


PassPhrase = "I want to learn cryptograph and network security"

BLOCKSIZE = 64                                             

numbytes = BLOCKSIZE // 8                                       


# Reduce the passphrase to a bit array of size BLOCKSIZE:

bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)  
                   
for i in range(0,len(PassPhrase) // numbytes):                  
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]           
    bv_iv ^= BitVector( textstring = textstr )                        


# Get key from user:

key = None

if sys.version_info[0] == 3:                                               
    key = input("\nEnter key: ")                                          
else:                                                                         
    key = raw_input("\nEnter key: ")                                        

key = key.strip()                                                                            


# Reduce the key to a bit array of size BLOCKSIZE:

key_bv = BitVector(bitlist = [0]*BLOCKSIZE)                   

for i in range(0,len(key) // numbytes):                        
    keyblock = key[i*numbytes:(i+1)*numbytes]                 
    key_bv ^= BitVector( textstring = keyblock )          



# Create a bitvector for storing the output plaintext bit array:

msg_decrypted_bv = BitVector( size = 0 )      


# Create a bitvector from the ciphertext hex string:


FILEIN = open(sys.argv[1])                                   
cipher = BitVector( hexstring = FILEIN.read().rstrip("\n") )   

   
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


# Write the decrypted plaintext to the output file:

FILEOUT = open(sys.argv[2], 'w')                               
FILEOUT.write(output_plaintext)                                      
FILEOUT.close() 


