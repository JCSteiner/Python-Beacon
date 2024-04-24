###############################################################################
# encode_buf.py
# used to encode the buffer given by C2
# This code is based on: https://github.com/RiverGumSecurity/PythonShellcode
# Modified by JCSteiner
###############################################################################

#%%## LOAD DEPENDENCIES
# our only dependency for this is numpy, we 
import numpy as np

###############################################################################
# RAW SHELLCODE HERE
# when you get your CS output, copy and paste the variable "buf" here as a 
# byte string.
###############################################################################
buf = b""

###############################################################################
# KEY FOR XOR HERE
# this is the key we will use for our xor
###############################################################################
key = "supersecret"

# Function to encrypt the buffer with an xor
def xor(data, k):
    # data - the shellcode that gets passed in
    # k    - the key used to xor the shellcode

    # calculates the number of times the key will have to repeat
    num_repeats = int(len(data) / len(k))

    # calculates the rest of the key since it may not repeat an even number of times
    remainder = len(data) % len(k)

    # extends the key to the proper length
    newkey = k * num_repeats + k[:remainder]

    # uses numpy to do a bitwise xor of the data with the key
    result = np.bitwise_xor(bytearray(data), bytearray(newkey))
    
    # returns the result
    return bytes(result)

# calculates the new buf variable after the xor
buf2 = xor(buf, key.encode())

# writes the new buf and the key to a text file
file = open("xor_buf.txt", "w")
file.write("rand_key = '" + key + "'\n")
file.write("rand_buf = " + str(buf2))
file.close()
