import numpy as np
import sounddevice as sd


#sd.default.device = (7, None)
print(sd.query_devices(), "\n")

# settings
fs = 48000
f0 = 18200        
f1 = 18400
f2 = 18000
tol = 50     
blocksize = 1024

bits = ""
previousBit = None
freqCount = 1
bitCount = 0

def byteToChar(byte):
    ascii_code = int(byte, 2)
    char = chr(ascii_code)
    return char
def allBitsToText(bits):
    text = ""
    for i in range(0, len(bits), 9):
        char = byteToChar(bits[i:i + 8])
        text += char
    return text
def add_bit(bit):
    """add bit to bits list and set spaces to seperate the bytes"""
    global bitCount, bits
    bits += str(bit)
    bitCount += 1
    if(bitCount == 8):
        print(byteToChar(bits[len(bits) - 8:len(bits)]), end="", flush=True)

        bits += " "
        bitCount =0


def getBit(freq, f0, f1, f2, tol):
    """check if freq is corresponding to f0 or f1 with a certain tolerance and return the corresponding bit (0 or 1)"""
    bit = None
    if(freq > f0 - tol and freq < f0 + tol):
        bit = 0
    elif(freq > f1 - tol and freq < f1 + tol):
        bit = 1 
    elif(freq > f2 - tol and freq < f2 + tol): # separation frequence
        bit = 2
    return bit

def getDominantFrequence(indata):
    """returns the dominant frequence from what the mic gets thanks to Fourier W Goat"""
    data = indata[:, 0]
    fft_vals = np.fft.rfft(data)
    fft_freqs = np.fft.rfftfreq(len(data), 1/fs)
    idx_max = np.argmax(np.abs(fft_vals))
    return int(fft_freqs[idx_max])


def getBinaryOutput(indata, frames, time, status):
    global bits, freqCount, bitCount, previousBit

    
    freq = getDominantFrequence(indata)
    bit = getBit(freq, f0, f1, f2, tol) # is current frequence absolute garbage or is it corresponding to f0, f1, or f2

    # the signal is composed with 3 frequences : f0, f1 and a separation frequence, f2. the f2 frequence only seperate
    # bits that are the same, if we have the sequence 00101110, the sound will be 02010121210, that way, there are never 
    # two consecutive frequences so we know when a new one is sent and we can decompose it without any shift issue
    # (notice that with this system, all frequences can have a different duration and it will still work)

    #every time a bit is different that the last one and the current bit is not a separation or a mic glitch, we add it
    if(bit != 2 and bit != None):
        freqCount += 1
        if(bit != previousBit and freqCount > 1):
            freqCount = 0
            add_bit(bit)

    previousBit = bit

    #print(allBitsToText(bits), freq, bit, bits)


with sd.InputStream(channels=1, callback=getBinaryOutput, samplerate=fs, blocksize=blocksize):
    print("balance le son")
    #infinite loop
    try:
        while True:
            pass
    except:
        print("\n",allBitsToText(bits))


