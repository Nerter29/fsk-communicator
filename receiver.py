import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt


sd.default.device = (6, None)
print(sd.query_devices())

# settings
fs = 48000
blocksize = 1024
f0 = 18000        
f1 = 19000
tol = 50     

# global shit
bits = ""
newBit = True

freqCount = 0
noneCount = 0

bitCount = 0

freqs = []

def add_bit(bit):
    """add bit to bits list and set spaces to seperate the bytes"""
    global bitCount, bits
    bits += str(bit)
    bitCount += 1
    if(bitCount == 8):
        bits += " "
        bitCount =0

def getBit(freq, f0, f1, tol):
    """check if freq is corresponding to f0 or f1 with a certain tolerance and return the corresponding bit (0 or 1)"""
    bit = None
    if(freq > f0 - tol and freq < f0 + tol):
        bit = 0
    elif(freq > f1 - tol and freq < f1 + tol):
        bit = 1 
    return bit

def getDominantFrequence(indata):
    """returns the dominant frequence from what the mic gets thanks to Fourier W Goat"""
    data = indata[:, 0]
    fft_vals = np.fft.rfft(data)
    fft_freqs = np.fft.rfftfreq(len(data), 1/fs)
    idx_max = np.argmax(np.abs(fft_vals))
    return float(fft_freqs[idx_max])


def getBinaryOutput(indata, frames, time, status):
    global bits, newBit, freqCount, noneCount, bitCount, freqs

    
    freq = getDominantFrequence(indata)
    bit = getBit(freq, f0, f1, tol) # is current frequence absolute garbage or is it corresponding to f0, or f1

    # the signal is composed with 3 frequences : f0, f1 and a separation frequence that can be anything, 
    # the function getBit() consider it as None.
    # it means that if we get a None in the signal, the next known frequence will be a new bit

    if(bit != None and newBit):
        newBit = False
        add_bit(bit)
    if(bit == None):
        newBit = True
    print(freq, bit, bits)


with sd.InputStream(channels=1, callback=getBinaryOutput, samplerate=fs, blocksize=blocksize):
    print("balance le son")
    #infinite loop
    while True:
        pass


















