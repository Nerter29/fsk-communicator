import numpy as np

def getBit(freq, f0, f1, tol):
    bit = None
    if(freq > f0 - tol and freq < f0 + tol):
        bit = 0
    elif(freq > f1 - tol and freq < f1 + tol):
        bit = 1 
    return bit
def getBinaryOutput(f, t, Sxx, f0, f1, tol):
    freqs = []
    for i in range(1,len(t)):
        index_max = np.argmax(Sxx[:, i])
        #time += float(t[i] - t[i-1])
        freq = (int(f[index_max]), float(round( t[i] - t[i-1], 5))) # actual freqence + its time on the record 
        freqs.append(freq)
    #print(freqs)
    bits = ""
    newBit = True
    freqCount = 0
    noneCount = 0
    bitCount = 0
    for i, freq in enumerate(freqs):
        bit = getBit(freq[0], f0, f1, tol)

        if( bit != None and newBit):
            noneCount = 0
            freqCount += 1
            if(freqCount > 2):
                newBit = False
                bits += str(bit)
                bitCount += 1
                if(bitCount == 8):
                    bits += " "
                    bitCount =0
        if( bit == None):
            freqCount = 0
            noneCount += 1
            if(noneCount >= 2):
                newBit = True

        if(i < 1000 and True):
            print(i, newBit, freqCount, freq, bit, bits)
    return bits
