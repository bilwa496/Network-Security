from encrypt_mtp import *

def decrypt_file(filename,key):
    ctFile = open(filename, 'r')
    ciphertexts = ctFile.readlines()
    cts = []
    for ct in ciphertexts:
        l = ct.rstrip('\n')
        if l != "":
            cts.append(l)
    pts = []
    for ct in cts:
        pts.append(decrypt(ct,key))
    print(pts)


def decrypt(cipher, key):
    cipher = (binascii.unhexlify(cipher.encode())).decode()
    msg = bxor(cipher, key)
    return msg


