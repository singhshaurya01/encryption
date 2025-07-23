# LOGISTIC MAP 
#The logistic map is a simple yet powerful equation used in chaos theory and population dynamics. Despite its simplicity, it can exhibit highly complex and even chaotic behavior. It generates a chaotic sequence 
#(keystream) which is XORD with the given data to produce chaotic data (stream cipher).
# Due to its simplicity, the method is much faster than complex cryptographic hash functions (like SHA-256), but less secure, unless combined with additional techniques.


import numpy as np

def logistic_map(r, x0, size):
    sequence = []
    x = x0
    for _ in range(size):
        x = r * x * (1 - x)
        sequence.append(x)
    return sequence

r = 3.99
x0 = 0.5 #SECRET HOTA YE.
seq = logistic_map(r, x0, 256*256)
