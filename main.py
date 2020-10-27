

import binascii, string
from random import *
from key_mtp import *
from encrypt_mtp import *
from decrypt_mtp import *

def main():
#since no plaintext or xihertext is provided in MTP question, we assume that Instructor will write the plaintexts into infile and that will be copied to ptFile
    ptFile = open("infile", 'r')
    plaintexts = ptFile.readlines()
    pts = [l.rstrip('\n') for l in plaintexts]

#to get the maximum length amongst all plaintexts
    max_len = max(len(m) for m in pts)
    k = generate_key(max_len)
    cts = []

    for msg in pts:
        cts.append(encrypt(msg,k) + "\n\n\n")

    outfile = open("outfile", 'w')
    outfile.writelines(cts)
    outfile.close()

    decrypt_file("outfile",k)


if __name__ == "__main__":
    main()

