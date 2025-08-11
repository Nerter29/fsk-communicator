import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.signal import spectrogram

from output import getBinaryOutput

def createSpectrogram(f, t, Sxx, data):
    if len(data.shape) > 1:
        data = data[:, 0]

    plt.figure(figsize=(10, 5))
    plt.pcolormesh(t, f, 10*np.log10(Sxx + 1e-10), shading='gouraud')
    plt.ylabel("Fréquence [Hz]")
    plt.xlabel("Temps [s]")
    plt.title("Spectrogramme")
    plt.colorbar(label="Intensité (dB)")
    plt.ylim(0, 21000)
    plt.savefig("spectrogramme.png")

def record():
    print("recording...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("done")
    wav.write("record.wav", fs, audio_data)


fs = 48000        
f0 = 18000        
f1 = 19000
tol = 50     

doRecord = 1

duration = 20
sd.default.device = (7, None)
#print(sd.query_devices())


if(doRecord == 1):
    record()

rate, data = wav.read("record.wav")
frequences, times, Sxx = spectrogram(data, fs=rate, nperseg=1024)
createSpectrogram(frequences, times, Sxx, data)

bits = getBinaryOutput(frequences, times, Sxx, f0, f1, tol)
print(bits)
