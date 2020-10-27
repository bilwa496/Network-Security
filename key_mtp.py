import string
from random import *

def generate_key(size):
    strk = ""
    for i in range(size):
        strk += string.ascii_letters[randint(0,51)]
    return strk  
